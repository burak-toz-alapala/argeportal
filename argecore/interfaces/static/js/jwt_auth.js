(() => {
    console.log("JWT Auth Loaded");


    function parseJwt(token) {
        try {
            return JSON.parse(atob(token.split('.')[1]));
        } catch (e) {
            return null;
        }
    }

    function logoutUser() {
        logout();
    }

    function checkTokenExpiration() {
        const token = sessionStorage.getItem("access");

        // Token yoksa => oturumu bitir
        if (!token) {
            console.warn("Token bulunamadı — logout yapılıyor.");
            logoutUser();
            return;
        }

        const decoded = parseJwt(token);
        // Decode edilemiyorsa veya exp yoksa => güvenlik için logout
        if (!decoded || !decoded.exp) {
            console.warn("Token geçersiz — logout yapılıyor.");
            logoutUser();
            return;
        }

        const expMs = decoded.exp * 1000;
        if (Date.now() >= expMs) {
            console.warn("Token süresi dolmuş — logout yapılıyor.");
            logoutUser();
        }
    }

    function refreshAccessToken() {
        const refresh = sessionStorage.getItem("refresh");
        if (!refresh) return;

        fetch("/auth/jwt/refresh/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ refresh }),
        })
            .then(res => {
                if (!res.ok) throw new Error();
                return res.json();
            })
            .then(data => {
                if (data.access) {
                    sessionStorage.setItem("access", data.access);
                }
            })
            .catch(logoutUser);
    }

    // sayfa ilk açıldığında
    checkTokenExpiration();

    // her 30 saniyede token kontrolü
    setInterval(() => {
        const token = sessionStorage.getItem("access");
        if (!token) return;

        const decoded = parseJwt(token);
        if (!decoded || !decoded.exp) return;

        const remaining = decoded.exp * 1000 - Date.now();

        if (remaining <= 0) {
            logoutUser();
            return;
        }

        if (remaining < 60000) {
            refreshAccessToken();
        }

    }, 30000);

})();
