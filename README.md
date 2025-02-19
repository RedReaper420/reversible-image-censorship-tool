# reversible-image-censorship-tool
Primitive visual encryption scripts for images.

## Preface
The idea to write a tool for reversible image censorship came to me when I decided to start moving to [Pixiv](https://www.pixiv.net/en/). I checked their rules and came across ones that require artists to censor genitals in their works, according to Japanese law (specifically, the infamous Article 175 of the Japanese Criminal Code). I'm against censorship, but if I want to upload my explicit works to the site, I have to obey the rules.

As an unorthodox compromise (after all I can just share links to uncensored works variants, duh), I came up with solutions of modifying images in the ways that severely distort the specified "obscene" regions, alike to black bars and pixelization ("mosaics"). Unlike the black bars and pixelization, which are irreversibly destroying the original image information, mine methods are only modifying it in a way that may be reverted to the original, uncensored image.

My methods are essentially the combination of primitive cryptography and steganography: the specified area of the image is being encrypted, and then an additional hidden information ("the key") in being added to the censored image for further automatic uncensoring (decryption of the distorted area, restoring to the original).

## Methods

The are 3 methods of reversible censorship which can be combined. Although, using just one is enough to conceal the specified area.
