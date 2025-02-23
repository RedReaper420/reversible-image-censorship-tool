# Reversible Image Censorship Tool
Primitive encryption and decryption scripts for PNG images.

## Preface
The idea to write a tool for reversible image censorship came to me when I decided to start moving to [Pixiv](https://www.pixiv.net/en/). I checked their rules and came across ones that require artists to censor genitals in their works, according to Japanese law (specifically, the infamous Article 175 of the Japanese Criminal Code). I'm against censorship, but if I want to upload my explicit works to the site, I have to obey the rules.

As an unorthodox compromise (after all, I can always just share links to uncensored works variants, duh), I came up with solutions of modifying images in the ways that severely distort the specified "obscene" regions, alike to black bars and pixelization ("mosaics"). But unlike the black bars and pixelization, which are irreversibly destroying the original image information, mine methods are only modifying it in a way that may be reverted to the original, uncensored image.

My methods are essentially the combination of primitive cryptography and steganography: the specified areas of the image are being encrypted, and then an additional hidden information ("the key") is being added to the censored image for further automatic uncensoring (decryption of the distorted areas, restoring to the original).

## Methods
There are 3 available methods of reversible censorship, which can be combined. Although, using just one is enough to conceal the specified area.

The PNG images below will be used for demonstrating the censorship methods. The pixel art one will be used in the orignal (small) resolution and upscaled after the transformation.
> [Handholding original source](https://x.com/suzuha00/status/1870830462266167516). [Silly pixel art meme by me](https://www.newgrounds.com/art/view/redreaperripper/so-true-bestie-pegs-you).


<img src="https://github.com/user-attachments/assets/16eeda68-eab8-43be-8b58-a7093714b30f" width="48%" height="auto">
<img src="https://github.com/user-attachments/assets/b3ec8a02-23ee-45e7-986f-adf322618ff5" width="48%" height="auto">
<img src="https://github.com/user-attachments/assets/01d2d195-0fef-4470-b906-21eacb19f6fc">

> `1st` image regions specification:
>
> [135](a "X position (from left)") [267](a "Y position (from top)") [69](a "Width (X size, to right)") [51](a "Height (Y size, to down)")
>
> 201 289 11 69
>
> 120 316 86 73

> `2nd` image region specification:
>
> 85 78 16 21

### "Mixing" method
This method changes the order of pixels in the specified area by transposing it 6 times, turning the region into a unified mess.

> [!CAUTION]
> The specified area should not be a perfect square, otherwise this method won't distort the area as intended.

<img src="https://github.com/user-attachments/assets/04f0a915-83e5-4207-8b51-1f798c1a1119" width="48%" height="auto">
<img src="https://github.com/user-attachments/assets/850fb43e-e34d-40bd-ad76-3beb80b14018" width="48%" height="auto">

### "Noising" method
This method adds a certain value to the color value according to the formula (takes pixel X and Y positions as arguments) and then performs modulo operation by 256. To additionally distort the specified region, a hue shift is being performed by swapping the color channels: R→G, G→B, B→R.

<img src="https://github.com/user-attachments/assets/14fbb2d1-6bde-4890-9a8f-2ae3d590b607" width="48%" height="auto">
<img src="https://github.com/user-attachments/assets/3ec4f166-c8f0-4e0c-8060-cfd534679b9f" width="48%" height="auto">

### "Hiding" method
This method just sets the alpha channel value of the specified area's pixels to 0, making the area fully transparent, yet still containing the color data.

> [!CAUTION]
> The specified area should not have transparent or semi-transparent pixels, otherwise this method will essentially corrupt the image, since there's no way to restore the original opacity level.

<img src="https://github.com/user-attachments/assets/6bc3ba5b-d69b-4130-befd-552ba48c4dde" width="48%" height="auto">
<img src="https://github.com/user-attachments/assets/9293deb3-beed-4886-8147-8015a00ba92d" width="48%" height="auto">

### Combining methods
Methods can be combined to scramble the specified area even further. Here is the result of using both the "mixing" and the "noising":

<img src="https://github.com/user-attachments/assets/82897748-8055-4fa5-8876-e8c977246c3b" width="48%" height="auto">
<img src="https://github.com/user-attachments/assets/3be368a9-053d-4725-a46e-b0798c680a85" width="48%" height="auto">

## Additional data hiding
When censoring the image, the last row of the image is being copied and added to the output image, this way increasing the image's height by 1 pixel. Into this additional row, a data necessary for automatic uncensoring is being injected. The information is being stored 1 bit per color channel of pixel.

The structure of the data row is such (from right to left)
| Pixels | R data | G data | B data |
| - | - | - | - |
| 1 | Mixing flag | Noising flag | [Scale mark](a "The first pixel contains 0, the second pixel contains 1. In case if the censored image will be upscaled by some integer number (pixel art upscaling, for example), the tool will detect it and still correctly uncensor the image.") |
| 1 | Hiding flag | - | Scale mark |
| 16 | Reg. 1 Position X | Reg. 2 Position X | Reg. 3 Position X | 
| 16 | Reg. 1 Position Y | Reg. 2 Position X | Reg. 3 Position X | 
| 16 | Reg. 1 Size X | Reg. 2 Position X | Reg. 3 Position X | 
| 16 | Reg. 1 Size Y | Reg. 2 Position X | Reg. 3 Position X | 

**Total:** 66 pixels. This way, the original image should be at least that wide so it can be censored (3 regions available). Each additional 64 pixels allow to add 3 more regions.

## Instruction
> [!IMPORTANT]
> Make sure that you have installed these:
> - [Python](https://www.python.org/)
> - [NumPy](https://numpy.org/)
> - [Pillow](https://pillow.readthedocs.io/en/latest/index.html)

For **censoring**:
1. Place an original PNG image into the directory with `main.py` as `original.png`
2. Run `main.py`
3. Enter 2
4. Enter the number of censored regions you're going to input
5. Enter (specified by you amount of times) 4 numbers separated with space: X position, Y position, X size, Y size
6. Enter a combination of three 1s and 0s separated with space to determine which methods to use
7. A `censored.png` image will appear in the same directory

For **uncensoring**:
1. Place a PNG image censored with this tool into the directory with `main.py` as `censored.png`
2. Run `main.py`
3. Enter 1
4. ???
5. PROFIT! Now an `uncensored.png` should appear in the same dir

## Afterword
I want to say thank you to people from Discord who gave me some hints on this tool implementation.
- "Noising" method (hue shift part): @unitrader
- "Hiding" method: @74363, @unitrader
- "Mixing" method: @reverse_mitts
- Additional data row: @tasadar2, @74363, @unitrader
