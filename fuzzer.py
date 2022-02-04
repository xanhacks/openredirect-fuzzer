#!/usr/bin/env python3
import argparse
from urllib.parse import urlparse
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

from requests import get
from requests.exceptions import InvalidSchema


disable_warnings(InsecureRequestWarning)


def fuzz(url, wordlist_path, cookies, http_proxy):
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'
	}
	proxies = {}

	if cookies:
		headers['Cookie'] = cookies
	if http_proxy:
		proxies['http'] = http_proxy
		proxies['https'] = http_proxy

	with open(wordlist_path, "r") as wordlist:
		for word in wordlist:
			payload = word.rstrip()

			print("Try payload :", payload)
			try:
				target_url = url.replace('FUZZ', payload)
				req = get(target_url, headers=headers, proxies=proxies, verify=False)

				if req.history:
					history_status = req.history[0].status_code
					history_headers = req.history[0].headers
					location = history_headers['Location'] if 'Location' in history_headers else ""
					print(f"=> {history_status} | Location : {location}, new URL : {req.url}")

					if urlparse(req.url).netloc != original_domain:
						print("=> Redirected to another domain !\n")
						break
					print()
				else:
					print(f"=> No redirection - {req.status_code} | URL : {req.url}\n")
			except InvalidSchema:
				print(f"=> Error - Invalid schema\n")
			except KeyboardInterrupt:
				print("\nExiting ...")
				break


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='OpenRedirect Fuzzer')

	parser.add_argument('-u', '--url', help='URL to attack (replace target parameter value by FUZZ).')
	parser.add_argument('-w', '--wordlist', help='Path to payload list file.')
	parser.add_argument('-c', '--cookies', help='Add cookies to all the requests.')
	parser.add_argument('-p', '--proxy', help='Set a proxy to all the requests.')

	args = parser.parse_args()

	original_domain = urlparse(args.url).netloc
	print("Start fuzzing ...")
	fuzz(args.url, args.wordlist, args.cookies, args.proxy)
