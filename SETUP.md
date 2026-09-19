
## 1. Put the files in your profile repo
Your profile repo must be named exactly like your username: `Rounak-Das-2007/Rounak-Das-2007`.
Upload everything from this folder (keep the `.github/workflows/` and `cache/` folders).

## 2. Create an access token
GitHub -> Settings -> Developer settings -> Personal access tokens -> Tokens (classic) -> Generate new token
Scopes: `repo`, `read:org`, `read:user`   (no expiry, or set a long one and renew it)

## 3. Add it as a secret
Profile repo -> Settings -> Secrets and variables -> Actions -> New repository secret
Name: `ACCESS_TOKEN`   Value: the token you just created

## 4. Let Actions push
Profile repo -> Settings -> Actions -> General -> Workflow permissions -> "Read and write permissions" -> Save

## 5. Run it once
Actions tab -> "README build" -> Run workflow. (Also run "Generate Contribution Snake".)
The first run counts lines of code for all your repos; after that it is cached and fast.

## Customising
* `build_card.py`    - edit the PROFILE rows (your info), then `python build_card.py`
* `today.py`         - change `UPTIME_SINCE` (the date the "Uptime" counter starts from)
* `make_ascii.py`    - turn your own photo/logo into the left-hand ASCII art:
                       `python make_ascii.py photo.jpg` then `python build_card.py`
                       (needs `pip install pillow lxml python-dateutil requests`)
