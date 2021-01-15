class AuthCheck {
    check_if_new_JWT() {
        const fragment = window.location.hash.substr(1).split('&')[0].split('=');
        if (fragment[0] === 'access_token') {
            this.token = fragment[1];
            localStorage.setItem('JWTS_LOCAL_KEY', this.token);
        }
    }

    load_jwts() {
        this.token = localStorage.getItem('JWTS_LOCAL_KEY') || null;
        if (this.token != null) {
            return this.token;
        } else {
            return false;
        }
    }

    logout() {
        this.token = '';
        localStorage.setItem('JWTS_LOCAL_KEY', this.token);
    }

    printToken() {
        var getJWT = localStorage.getItem('JWTS_LOCAL_KEY');
        console.log(getJWT);
    }

    parseJwt(token) {
        var base64Url = token.split('.')[1];
        var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        var jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
            return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
        }).join(''));

        return JSON.parse(jsonPayload);
    };

    checkPrem(premission) {
        if (this.load_jwts()) {
            var premissions = this.parseJwt(this.load_jwts())['permissions'];
            console.log(premissions);
            if ($.inArray(premission, premissions) != -1) {
                return true;
            } else {
                return false;
            }
        } else {
            return false;
        }
    }
}