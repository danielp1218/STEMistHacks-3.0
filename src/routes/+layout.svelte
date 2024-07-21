<script lang="ts">
	import { AppBar, AppLayout, NavItem, settings } from "svelte-ux";

	import { page } from '$app/stores';
	import '../app.postcss';

	settings({
		components: {
			AppLayout: {
				classes: {
					aside: 'border-r',
					nav: 'bg-surface-300 py-2',
				},
			},
			NavItem: {
				classes: {
					root: 'text-sm text-surface-content/70 pl-6 py-2 hover:bg-surface-100/70 relative',
					active:
						'text-primary bg-surface-100 font-medium before:absolute before:bg-primary before:rounded-full before:w-1 before:h-2/3 before:left-[6px] shadow z-10',
				},
			},
		},
	});

</script>

<AppLayout>
	<svelte:fragment slot="nav">
		<NavItem
			path="/"
			text="Home"
			icon="M10,20V14H14V20H19V12H22L12,3L2,12H5V20H10Z"
			currentUrl={$page.url}
		/>

		<NavItem
			path="/stats"
			text="Stats"
			icon="M22,21H2V3H4V15.54L9.5,6L16,9.78L20.24,2.45L21.97,3.45L22,21Z"
			currentUrl={$page.url}
		/>

		<NavItem
			path="/crypto"
			text="Crypto"
			icon="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"
			currentUrl={$page.url}
		/>
	</svelte:fragment>

	<AppBar title="App Name" class="bg-primary-100 text-primary-contentG">
	</AppBar>

	<slot />
</AppLayout>
<footer>
	<img src="/bottom%20banner.png" alt="Cat Banner"/>
</footer>

<style>
	footer {
		position: fixed;
		bottom: 0;
		left: 0;
		right: 0;
		pointer-events: none;
	}
</style>