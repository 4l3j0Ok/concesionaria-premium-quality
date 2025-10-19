import { APP_VERSION } from "astro:env/client";
import { API_URL } from "astro:env/server";

export class Application {
    static name = "Premium Quality";
    static version = APP_VERSION;
    static apiURL = API_URL;
    static githubUrl = "https://github.com/4l3j0Ok";
    static linkedinUrl = "https://www.linkedin.com/in/alejoide";
    static email = "contacto@alejoide.com";
}