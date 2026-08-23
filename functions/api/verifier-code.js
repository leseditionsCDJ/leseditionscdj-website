const encoder = new TextEncoder();

function normalizeCode(value) {
    return String(value || "")
        .trim()
        .toLowerCase()
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "");
}

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

async function createToken(secret, expires) {
    const data = `tina:${expires}`;

    const key = await crypto.subtle.importKey(
        "raw",
        encoder.encode(secret),
        {
            name: "HMAC",
            hash: "SHA-256"
        },
        false,
        ["sign"]
    );

    const signature = await crypto.subtle.sign(
        "HMAC",
        key,
        encoder.encode(data)
    );

    const signatureBase64 = bytesToBase64Url(
        new Uint8Array(signature)
    );

    return `${expires}.${signatureBase64}`;
}

export async function onRequestPost(context) {
    try {

        if (
            !context.env.CODE_TINA ||
            !context.env.SESSION_SECRET
        ) {
            return Response.json(
                {
                    success: false,
                    message: "Configuration du serveur incomplète."
                },
                {
                    status: 500,
                    headers: {
                        "Cache-Control": "no-store"
                    }
                }
            );
        }


        const body = await context.request.json();

        const enteredCode =
            normalizeCode(body.code);

        const tinaCode =
            normalizeCode(context.env.CODE_TINA);


        if (enteredCode !== tinaCode) {

            return Response.json(
                {
                    success: false,
                    message: "Ce code secret n'est pas reconnu."
                },
                {
                    status: 401,
                    headers: {
                        "Cache-Control": "no-store"
                    }
                }
            );

        }


        /*
        =========================
        LANGUE
        =========================

        La page anglaise envoie :
        lang: "en"

        La page française n'envoie rien,
        donc le français reste la langue
        par défaut.
        */

        const language =
            body.lang === "en"
                ? "en"
                : "fr";


        const redirect =
            language === "en"
                ? "/en/espace-tina/"
                : "/espace-tina/";


        /*
        =========================
        AUTORISATION
        =========================

        Valide pendant 30 jours.
        */

        const maxAge =
            60 * 60 * 24 * 30;

        const expires =
            Math.floor(Date.now() / 1000) +
            maxAge;


        const token =
            await createToken(
                context.env.SESSION_SECRET,
                expires
            );


        return Response.json(
            {
                success: true,
                redirect: redirect
            },
            {
                status: 200,

                headers: {

                    /*
                    Path=/ permet au même accès
                    de fonctionner pour :

                    /espace-tina/

                    ET

                    /en/espace-tina/
                    */

                    "Set-Cookie":
                        `cdj_tina=${token}; ` +
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


    } catch (error) {

        return Response.json(
            {
                success: false,
                message: "Une erreur est survenue."
            },
            {
                status: 500,
                headers: {
                    "Cache-Control": "no-store"
                }
            }
        );

    }
}
