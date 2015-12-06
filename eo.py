import json
import os
import random
import requests

"""
  here is a wrapper for the *unreleased* electric objects API
  Built by Harper Reed (harper@nata2.org) - @harper

  Hopefully someday a real API will appear

"""

CREDENTIALS_FILE = '.credentials'
USER_ENV_VAR = 'EO_USER'
PASSWORD_ENV_VAR = 'EO_PASS'


class electric_object:
    base_url = 'https://www.electricobjects.com/'

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def make_request(self, url, params=None, method='GET', ):
        with requests.Session() as s:
            eo_sign = s.get('https://www.electricobjects.com/sign_in')
            authenticity_token = eo_sign.text.encode('utf-8').strip().split("type=\"hidden\" name=\"authenticity_token\" value=\"")[1].split("\" />")[0]
            payload = {
                "user[email]": self.username,
                "user[password]": self.password
            }
            payload['authenticity_token'] = authenticity_token
            p = s.post('https://www.electricobjects.com/sign_in', data=payload)
            if p.status_code == 200:
                url = self.base_url + url
                # An authorised request.
                if method == "GET":
                    r = s.get(url)
                elif method == "POST":
                    r = s.post(url, params=params)
                elif method == "PUT":
                    r = s.put(url)
                elif method == "DELETE":
                    r = s.delete(url)

                if r.status_code == 204:
                    return True
                else:
                    return r.text.encode('utf-8').strip()

    # Set a media as a favorite
    def user(self):
        url = "/api/beta/user/"
        return self.make_request(url, method='GET')

    # Set a media as a favorite
    def favorite(self, media_id):
        url = "/api/beta/user/artworks/favorited/" + media_id
        return self.make_request(url, method='PUT')

    # Remove a media as a favorite
    def unfavorite(self, media_id):
        url = "/api/beta/user/artworks/favorited/" + media_id
        return self.make_request(url, method='DELETE')

    # Display a piece of media
    def display(self, media_id):
        url = "/api/beta/user/artworks/displayed/" + media_id
        return self.make_request(url, method='PUT')

    def favorites(self):
        url = "/api/beta/user/artworks/favorited"
        favorites_json = json.loads(self.make_request(url, method='GET'))
        return favorites_json

    # Display a piece of media
    def display_random_favorite(self):
        favs = self.favorites()
        fav = random.choice(favs)
        media_id = str(fav['artwork']['id'])
        print media_id
        return self.display(media_id)

    # Set a url to be on the display
    # IN PROGRESS
    def set_url(self, url):
        url = "set_url"
        with requests.Session() as s:
            eo_sign = s.get('https://www.electricobjects.com/sign_in')
            authenticity_token = eo_sign.text.encode('utf-8').strip().split("name=\"authenticity_token\" type=\"hidden\" value=\"")[1].split("\" /></div>")[0]
            payload = {
                "user[email]": self.username,
                "user[password]": self.password
            }
            payload['authenticity_token'] = authenticity_token
            p = s.post('https://www.electricobjects.com/sign_in', data=payload)
            if p.status_code == 200:
                eo_sign = s.get('https://www.electricobjects.com/set_url')
                authenticity_token = eo_sign.text.encode('utf-8').strip().split("name=\"authenticity_token\" type=\"hidden\" value=\"")[1].split("\" /></div>")[0]
                print authenticity_token
                params = {
                  "custom_url": url,
                  "authenticity_token": authenticity_token
                }
                r = s.post(self.base_url + url, params=params)
                if r.status_code == 200:
                    return True
                else:
                    return False


# Obtains the electricobjects.com username and password. They can be set here in the code,
# in environment variables, or in a file named by CREDENTIALS_FILE.
# A simple way to set them in the environment variables is prefix your command with them.
# For example:
#     $ EO_USER=you@example.com EO_PASS=pword python eo.py
#
# Don't forget to clear your command history if you don't want the credentials stored.
#
# This function allows us to avoid uploading credentials to GitHub. In addition to not
# writing them here, the credentials filename is included in the .gitignore file.
#
# The sources are read in the order of: default, then environment variables, then file.
# Each source overwrites the username and password separately, if set in that source.
#
def get_credentials():
    username = ''  # You can set them here if you don't plan on uploading to GitHub.
    password = ''

    username = os.environ[USER_ENV_VAR] if USER_ENV_VAR in os.environ else username
    password = os.environ[PASSWORD_ENV_VAR] if PASSWORD_ENV_VAR in os.environ else password

    try:
        with open(CREDENTIALS_FILE, 'r') as f:
            username = next(f).strip()
            password = next(f).strip()
    except:
        pass  # Fail silently if no file, missing lines, or other problem.

    return {"username": username, "password": password}


if __name__ == "__main__":
    # How to use this dude:
    # instantiate it. yay!
    credentials = get_credentials()
    eo = electric_object(username=credentials["username"], password=credentials["password"])
    favs = eo.display_random_favorite()

    # Let's favorite and unfavorite medias:
    # now favorite
    # print eo.favorite("5626")
    # now unfavorite
    # print eo.unfavorite("5626")

    # Displaying in
    # Display a URL
    # art = ['5568','1136']
    # print eo.display("1136")

    # Let's set a url
    # print eo.set_url("http://www.harperreed.com/")
