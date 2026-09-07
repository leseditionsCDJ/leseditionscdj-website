const encoder = new TextEncoder();


/* =========================
   NORMALISATION DU CODE
========================= */

function normalizeCode(value) {

    return String(value || "")
        .trim()
        .toLowerCase()
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "");

}


/* =========================
   BASE64 URL
========================= */

function bytesToBase64Url(bytes) {

    let binary = "";

    for (const byte of bytes) {
        binary += String.fromCharCode(byte);
    }

    return btoa(binary)
        .replace(/\+/g, "-")
        .replace(/\//g, "_")
        .replace(/=+$/g, "");

}


/* =========================
   CRÉATION DU TOKEN
========================= */

async function createToken(
    secret,
    espace,
    expires
) {

    /*
    Le token contient maintenant
    le nom de l'espace.

    Exemples :

    tina:123456789
    edouard:123456789
    */

    const data =
        `${espace}:${expires}`;


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
            encoder.encode(data)
        );


    const signatureBase64 =
        bytesToBase64Url(
            new Uint8Array(signature)
        );


    return `${expires}.${signatureBase64}`;

}



/* =========================
   VÉRIFICATION DU CODE
========================= */

export async function onRequestPost(context) {

    try {


        /* =========================
           CONFIGURATION
        ========================== */

        if (!context.env.SESSION_SECRET) {

            return Response.json(
                {
                    success: false,
                    message:
                        "Configuration du serveur incomplète."
                },
                {
                    status: 500,
                    headers: {
                        "Cache-Control":
                            "no-store"
                    }
                }
            );

        }


        const body =
            await context.request.json();


        const enteredCode =
            normalizeCode(body.code);



        /* =========================
           CODES DES TOMES
        ========================== */

        const tinaCode =
            normalizeCode(
                context.env.CODE_TINA
            );


        const edouardCode =
            normalizeCode(
                context.env.CODE_EDOUARD
            );



        /* =========================
           IDENTIFIER LE TOME
        ========================== */

        let espace = null;


        if (
            tinaCode &&
            enteredCode === tinaCode
        ) {

            espace = "tina";

        }


        else if (
            edouardCode &&
            enteredCode === edouardCode
        ) {

            espace = "edouard";

        }


        else {

            return Response.json(
                {
                    success: false,
                    message:
                        "Ce code secret n'est pas reconnu."
                },
                {
                    status: 401,
                    headers: {
                        "Cache-Control":
                            "no-store"
                    }
                }
            );

        }



        /* =========================
           LANGUE
        ==========================

        La page anglaise envoie :

        lang: "en"

        Sinon, le français est utilisé.
        */

        const language =
            body.lang === "en"
                ? "en"
                : "fr";



        /* =========================
           REDIRECTION
        ========================== */

        let redirect;


        if (espace === "tina") {

            redirect =
                language === "en"
                    ? "/en/espace-tina/"
                    : "/espace-tina/";

        }


        else if (espace === "edouard") {

            redirect =
                language === "en"
                    ? "/en/espace-edouard/"
                    : "/espace-edouard/";

        }



        /* =========================
           COOKIE
        ========================== */

        const cookieName =
            espace === "tina"
                ? "cdj_tina"
                : "cdj_edouard";



        /* =========================
           DURÉE D'AUTORISATION
        ==========================

        Accès valide pendant 30 jours.
        */

        const maxAge =
            60 * 60 * 24 * 30;


        const expires =
            Math.floor(
                Date.now() / 1000
            ) +
            maxAge;



        /* =========================
           CRÉATION DU TOKEN
        ========================== */

        const token =
            await createToken(
                context.env.SESSION_SECRET,
                espace,
                expires
            );



        /* =========================
           RÉPONSE
        ========================== */

        return Response.json(
            {
                success: true,
                redirect: redirect
            },
            {
                status: 200,

                headers: {

                    "Set-Cookie":
                        `${cookieName}=${token}; ` +
                        `Path=/; ` +
                        `Max-Age=${maxAge}; ` +
                        `HttpOnly; ` +
                        `Secure; ` +
                        `SameSite=Lax`,

                    "Cache-Control":
                        "no-store"
                }
            }
        );


    }

    catch (error) {


        return Response.json(
            {
                success: false,
                message:
                    "Une erreur est survenue."
            },
            {
                status: 500,

                headers: {
                    "Cache-Control":
                        "no-store"
                }
            }
        );

    }

}
