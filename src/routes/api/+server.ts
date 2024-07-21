import { error } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import {SECRET_API_KEY} from "$env/static/private";

export const POST: RequestHandler = async ({ url }) => {
	const wallet = (url.searchParams.get('wallet_address')) as string;

	const formData = new FormData();

	formData.append('allowPlatformToOperateToken', 'true');
	formData.append('chain', 'sepolia');
	formData.append('data', 'pet');
	formData.append("recipientAddress", wallet);

	const endpoint = 'https://api.verbwire.com/v1/nft/mint/quickMintFromMetadata';;
	const options = {
		method: 'POST',
		headers: {
			accept: 'application/json',
			'X-API-Key': SECRET_API_KEY
		}
	};

	await fetch(endpoint, {
		body: formData,
		...options
	})
		.then(res => res.json())
		.then(json => console.log(json))
		.catch(err => console.error('error:' + err));

	return new Response()
};