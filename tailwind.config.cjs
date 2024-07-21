const colors = require("tailwindcss/colors");
const svelte_ux = require("svelte-ux/plugins/tailwind.cjs");

/** @type {import("tailwindcss").Config}*/
const config = {
	content: [
		"./src/**/*.{html,svelte}",
		"./node_modules/svelte-ux/**/*.{svelte,js}",
		"./node_modules/layerchart/**/*.{svelte,js}"
	],
	theme: {
		extend: {}
	},
	variants: {
		extend: {}
	},
	plugins: [svelte_ux],
	ux: {
		themes: {
			light: {
				"color-scheme": "light",
				primary: "hsl(170,41%,44%)",
				secondary: "hsl(81.3699 52.518% 72.7451%)",
				accent: "hsl(323.1325 72.1739% 77.451%)",
				neutral: "hsl(214.2857 19.6262% 20.9804%)",
				"surface-100": "hsl(37.5 36.3636% 95.6863%)",
				"surface-200": "hsl(0 0% 94.902%)",
				"surface-300": "hsl(180 1.9608% 90%)"
			},
			dark: {
				"color-scheme": "light",
				primary: "hsl(170,41%,44%)",
				secondary: "hsl(81.3699 52.518% 72.7451%)",
				accent: "hsl(323.1325 72.1739% 77.451%)",
				neutral: "hsl(214.2857 19.6262% 20.9804%)",
				"surface-100": "hsl(37.5 36.3636% 95.6863%)",
				"surface-200": "hsl(0 0% 94.902%)",
				"surface-300": "hsl(180 1.9608% 90%)"
			}
		}
	}
};

module.exports = config;
