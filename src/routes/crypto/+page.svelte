<script lang="ts">
	import { Button, Input } from "svelte-ux";

	let wallet_address = "";

	const getNft = async () => {
		const response = await fetch(`/api?wallet_address=${wallet_address}`);
	}
</script>

<main class="p-4">
	<h1 class="text-4xl font-bold pt-8 pb-4">Earn Passive Income</h1>
	<h2 class="text-xl pb-16">Help us research by providing us data and receive <span
		class="font-bold text-accent">$FTM</span> as a reward!</h2>
	<h1 class="text-2xl font-bold pb-4">Wallet Address</h1>
	<form>
		<Input bind:value={wallet_address} label="Wallet Address" placeholder="0x..." class="border-2 border-primary-200 px-2 py-4 rounded-2xl text-xl"/>
	</form>
	<Button class="w-full text-2xl py-4 my-8 rounded-2xl" variant="fill" color="accent" on:click={getNft}>Get NFT</Button>
</main>
