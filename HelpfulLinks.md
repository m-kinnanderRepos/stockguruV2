# Sites that helped me build stockGuru

stockGuru is a program to help monitor your stocks. These are sites I found helfpul when I created this project. I hope you too find them helpful or learn something new from one of them.

### In no particular order.

## [How to write unittests](https://codefather.tech/blog/write-unit-test-python/)

## [python requests guide](https://realpython.com/python-requests/)

## [pyenv not changing python version](https://github.com/pyenv/pyenv/issues/849)

I had issues getting pyenv to work. I don't think I followed the setup instructions from pyenv first.
The answer from chriswininger commented on Jul 26, 2021 helped me finish set up.
If you run into errors too, trying answers from this page should help you.

## [Finage api documentation](https://finage.co.uk/docs/api/us-stock-historical-end-of-day-data)

I first used a couple other stock apis but I found Finage to be the best. Their documentation is helpful and they had endpoints that I needed (historical) and their free subscription was much appreciated. The `main` branch is based off of the free subscription because of the limitations the free subscription tier has (mainly 15 second delay between calls).

- I will create a seperate branch (no ETA for this right now) that utilizes a higher tier subscription that contains more logic that I couldn't do with the free subscription.

## [How to use pyenv](https://realpython.com/intro-to-pyenv/)

I enjoy this article and referenced it frequently until I memorized commands.

## [Managing virtual envs with pyenv](https://towardsdatascience.com/managing-virtual-environment-with-pyenv-ae6f3fb835f8)

I kept getting squiggles under `import requests`. This page has a section on `Using your environment in IDEs` which removed the troubling squiggles.

## [Python requests.Response Object](https://www.w3schools.com/python/ref_requests_response.asp)

During testing I needed to know exactly what properties/methods were available with the response.

## [How to make a readme](https://www.makeareadme.com/)

I knew you could use `#` for formatting but it wasn't clear to me. A google search brought this page up first and it was helpful enough that I haven't searched for more examples.
