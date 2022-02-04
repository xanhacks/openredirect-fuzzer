#!/usr/bin/env python3
import argparse

from request import get


def fuzz(url, wordlist_path, cookies):
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'
	}
	if cookies: headers['Cookies'] = cookies

	with open(wordlist_path, "r") as wordlist:
		for word in wordlist:
			payload = word.rstrip()
			
			target_url = url.replace('FUZZ', payload)
			req = get(target_url, headers=headers)

			if req.history:
				history_status = req.history[0].status_code
				history_headers = req.history[0].headers
				location = history_headers['Location'] if 'Location' in history_headers else ""
				print(f"[{history_status}] Location : {location}, new URL : {req.url}, payload : {payload}")
			print(f"[No redirection - {req.status_code}] URL : {req.url}, payload : {payload}")


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='OpenRedirect Fuzzer')

	parser.add_argument('-u', '--url', help='URL to attack (replace target parameter value by FUZZ).')
	parser.add_argument('-w', '--wordlist', help='Path to payload list file.')
	parser.add_argument('-c', '--cookies', help='Add cookies to all the requests.')

	args = parser.parse_args()

	print("Start fuzzing ...")
	fuzz(args.url, args.wordlist, args.cookies)
