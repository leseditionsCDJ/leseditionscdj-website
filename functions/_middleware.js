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


    if (url.pathname === "/en" || url.pathname.startsWith("/en/")) {
        const destination = new URL("/", url);
        return new Response(null, {
            status: 301,
            headers: { Location: destination.toString() }
        });
    }

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


    const isFrenchFlorentSpace =
        url.pathname === "/espace-florent" ||
        url.pathname.startsWith("/espace-florent/");


    /*
    =========================
    IDENTIFIER L'ESPACE
    =========================
    */

    let espace = null;

    let cookieName = null;


    if (
        isFrenchTinaSpace
    ) {

        espace = "tina";

        cookieName =
            "cdj_tina";

    }


    else if (
        isFrenchEdouardSpace
    ) {

        

        espace = "edouard";

        cookieName =
            "cdj_edouard";

    }


    else if (isFrenchFlorentSpace) {

        espace = "florent";
        cookieName = "cdj_florent";

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
            "/code-secret.html";


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
