const encoder = new TextEncoder();


function getCookies(request, name) {

    const cookieHeader =
        request.headers.get("Cookie");

    if (!cookieHeader) {
        return [];
    }

    const values = [];

    const cookies =
        cookieHeader.split(";");

    for (const cookie of cookies) {

        const [key, ...valueParts] =
            cookie.trim().split("=");

        if (key === name) {

            values.push(
                valueParts.join("=")
            );

        }
    }

    return values;
}


function base64UrlToBytes(value) {

    let base64 = value
        .replace(/-/g, "+")
        .replace(/_/g, "/");

    while (base64.length % 4) {
        base64 += "=";
    }

    const binary =
        atob(base64);

    const bytes =
        new Uint8Array(binary.length);

    for (
        let i = 0;
        i < binary.length;
        i++
    ) {

        bytes[i] =
            binary.charCodeAt(i);

    }

    return bytes;
}


async function verifyToken(
    token,
    secret,
    espace
) {

    try {

        if (!token || !secret) {
            return false;
        }

        const parts =
            token.split(".");

        if (parts.length !== 2) {
            return false;
        }

        const expires =
            Number(parts[0]);

        const signature =
            parts[1];

        if (!Number.isFinite(expires)) {
            return false;
        }

        const now =
            Math.floor(
                Date.now() / 1000
            );

        if (expires <= now) {
            return false;
        }


        /*
        Le nom de l'espace doit
        correspondre à celui utilisé
        dans verifier-code.js :

        tina
        edouard
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

                ["verify"]
            );


        return await crypto.subtle.verify(

            "HMAC",

            key,

            base64UrlToBytes(
                signature
            ),

            encoder.encode(data)
        );


    } catch (error) {

        return false;

    }
}


export async function onRequest(context) {

    const url =
        new URL(
            context.request.url
        );


    /*
    =========================
    ESPACE TINA FRANÇAIS
    =========================
    */

    const isFrenchTinaSpace =

        url.pathname ===
            "/espace-tina"

        ||

        url.pathname.startsWith(
            "/espace-tina/"
        );


    /*
    =========================
    ESPACE TINA ANGLAIS
    =========================
    */

    const isEnglishTinaSpace =

        url.pathname ===
            "/en/espace-tina"

        ||

        url.pathname.startsWith(
            "/en/espace-tina/"
        );


    /*
    =========================
    ESPACE ÉDOUARD FRANÇAIS
    =========================
    */

    const isFrenchEdouardSpace =

        url.pathname ===
            "/espace-edouard"

        ||

        url.pathname.startsWith(
            "/espace-edouard/"
        );


    /*
    =========================
    ESPACE EDWARD ANGLAIS
    =========================
    */

    const isEnglishEdwardSpace =

        url.pathname ===
            "/en/espace-edward"

        ||

        url.pathname.startsWith(
            "/en/espace-edward/"
        );


    /*
    =========================
    IDENTIFIER L'ESPACE
    =========================
    */

    let espace = null;

    let cookieName = null;

    let isEnglishSpace = false;


    if (
        isFrenchTinaSpace ||
        isEnglishTinaSpace
    ) {

        espace = "tina";

        cookieName =
            "cdj_tina";

        isEnglishSpace =
            isEnglishTinaSpace;

    }


    else if (
        isFrenchEdouardSpace ||
        isEnglishEdwardSpace
    ) {

        /*
        Même si le personnage
        s'appelle Edward en anglais,
        le nom interne du token
        reste "edouard".
        */

        espace = "edouard";

        cookieName =
            "cdj_edouard";

        isEnglishSpace =
            isEnglishEdwardSpace;

    }


    /*
    =========================
    PAGE PUBLIQUE
    =========================
    */

    if (!espace) {

        return context.next();

    }


    /*
    =========================
    VÉRIFICATION DU COOKIE
    =========================
    */

    const tokens =
        getCookies(
            context.request,
            cookieName
        );


    let authorized = false;


    for (const token of tokens) {

        const valid =
            await verifyToken(
                token,
                context.env.SESSION_SECRET,
                espace
            );

        if (valid) {

            authorized = true;

            break;

        }

    }


    /*
    =========================
    PAS D'AUTORISATION
    =========================
    */

    if (!authorized) {


        const secretCodePage =
            isEnglishSpace
                ? "/en/code-secret.html"
                : "/code-secret.html";


        const redirectUrl =
            new URL(
                secretCodePage,
                context.request.url
            );


        redirectUrl.searchParams.set(
            "acces",
            "refuse"
        );


        return new Response(
            null,
            {
                status: 302,

                headers: {

                    "Location":
                        redirectUrl.toString(),

                    "Cache-Control":
                        "no-store"
                }
            }
        );

    }


    /*
    =========================
    AUTORISATION VALIDE
    =========================
    */

    return context.next();

}
