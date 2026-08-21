const encoder = new TextEncoder();

function getCookie(request, name) {
    const cookieHeader = request.headers.get("Cookie");

    if (!cookieHeader) {
        return null;
    }

    const cookies = cookieHeader.split(";");

    for (const cookie of cookies) {
        const [key, ...valueParts] = cookie.trim().split("=");

        if (key === name) {
            return valueParts.join("=");
        }
    }

    return null;
}

function base64UrlToBytes(value) {
    let base64 = value
        .replace(/-/g, "+")
        .replace(/_/g, "/");

    while (base64.length % 4) {
        base64 += "=";
    }

    const binary = atob(base64);
    const bytes = new Uint8Array(binary.length);

    for (let i = 0; i < binary.length; i++) {
        bytes[i] = binary.charCodeAt(i);
    }

    return bytes;
}

async function verifyToken(token, secret) {
    try {
        if (!token || !secret) {
            return false;
        }

        const parts = token.split(".");

        if (parts.length !== 2) {
            return false;
        }

        const expires = Number(parts[0]);
        const signature = parts[1];

        if (!Number.isFinite(expires)) {
            return false;
        }

        const now = Math.floor(Date.now() / 1000);

        if (expires <= now) {
            return false;
        }

        const data = `tina:${expires}`;

        const key = await crypto.subtle.importKey(
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
            base64UrlToBytes(signature),
            encoder.encode(data)
        );

    } catch (error) {
        return false;
    }
}

export async function onRequest(context) {
    const url = new URL(context.request.url);

    const isTinaSpace =
        url.pathname === "/espace-tina" ||
        url.pathname.startsWith("/espace-tina/");

    // Tout le reste du site reste public
    if (!isTinaSpace) {
        return context.next();
    }

    const token = getCookie(context.request, "cdj_tina");

    const authorized = await verifyToken(
        token,
        context.env.SESSION_SECRET
    );

    // Pas d'autorisation valide
    if (!authorized) {
        const redirectUrl = new URL(
            "/code-secret.html",
            context.request.url
        );

        redirectUrl.searchParams.set("acces", "refuse");

        return new Response(null, {
            status: 302,
            headers: {
                "Location": redirectUrl.toString(),
                "Cache-Control": "no-store"
            }
        });
    }

    // Autorisation valide : afficher normalement la page
    return context.next();
}
