function jsonResponse(data, status = 200, extraHeaders = {}) {

    return new Response(
        JSON.stringify(data),
        {
            status: status,

            headers: {
                "Content-Type": "application/json; charset=UTF-8",
                "Cache-Control": "no-store",
                ...extraHeaders
            }
        }
    );

}


/*
    Permet d'accepter par exemple :

    pastèque
    PASTÈQUE
    Pasteque

    Ce sera plus facile pour les enfants.
*/

function normalizeCode(value) {

    return String(value || "")
        .trim()
        .toLowerCase()
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "")
        .normalize("NFC");

}


/*
    Transforme la signature en texte
    pouvant être placé dans un cookie.
*/

function toBase64Url(bytes) {

    let binary = "";

    for (const byte of bytes) {
        binary += String.fromCharCode(byte);
    }

    return btoa(binary)
        .replace(/\+/g, "-")
        .replace(/\//g, "_")
        .replace(/=+$/g, "");

}


/*
    Crée une signature sécurisée
    avec notre secret Cloudflare.
*/

async function createSignature(secret, message) {

    const encoder =
        new TextEncoder();


    const key =
        await crypto.subtle.importKey(
            "raw",
            encoder.encode(secret),
            {
                name: "HMAC",
                hash: "SHA-256"
            },
            false,
            ["sign"]
        );


    const signature =
        await crypto.subtle.sign(
            "HMAC",
            key,
            encoder.encode(message)
        );


    return toBase64Url(
        new Uint8Array(signature)
    );

}



/*
    Cette fonction répond uniquement
    aux requêtes POST envoyées par
    code-secret.html.
*/

export async function onRequestPost(context) {


    let body;


    try {

        body =
            await context.request.json();

    }

    catch (error) {

        return jsonResponse(
            {
                success: false,
                message: "Requête invalide."
            },
            400
        );

    }



    const enteredCode =
        normalizeCode(body.code);


    if (!enteredCode) {

        return jsonResponse(
            {
                success: false,
                message: "Aucun code n'a été entré."
            },
            400
        );

    }



    /*
        Les vraies valeurs seront enregistrées
        dans les Secrets Cloudflare.

        Elles ne seront PAS écrites dans GitHub.
    */

    const tinaCode =
        normalizeCode(
            context.env.CODE_TINA
        );


    const sessionSecret =
        context.env.SESSION_SECRET;



    /*
        Si les secrets Cloudflare
        ne sont pas configurés.
    */

    if (!tinaCode || !sessionSecret) {

        console.error(
            "Les secrets Cloudflare ne sont pas configurés."
        );


        return jsonResponse(
            {
                success: false,
                message: "Configuration du serveur incomplète."
            },
            500
        );

    }



    /*
        =========================
        TOME 1 — TINA
        =========================
    */

    if (enteredCode === tinaCode) {


        /*
            L'autorisation reste valide
            pendant 1 an sur cet appareil.

            Si les cookies sont supprimés,
            il suffira de rentrer le code
            du livre de nouveau.
        */

        const expiration =
            Math.floor(Date.now() / 1000)
            +
            (60 * 60 * 24 * 365);



        const payload =
            `tina.${expiration}`;



        const signature =
            await createSignature(
                sessionSecret,
                payload
            );



        const token =
            `${payload}.${signature}`;



        const cookie =
            [
                `cdj_tina=${encodeURIComponent(token)}`,
                "Path=/",
                "Max-Age=31536000",
                "HttpOnly",
                "Secure",
                "SameSite=Lax"
            ].join("; ");



        return jsonResponse(
            {
                success: true,

                redirect:
                    "/espace-tina/"
            },
            200,
            {
                "Set-Cookie": cookie
            }
        );

    }



    /*
        =========================
        CODE INCONNU
        =========================
    */

    return jsonResponse(
        {
            success: false,
            message: "Code non reconnu."
        },
        401
    );

}
