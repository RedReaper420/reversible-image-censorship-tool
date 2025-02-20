# reversible-image-censorship-tool
Primitive encryption and decryption scripts for PNG images.

## Preface
The idea to write a tool for reversible image censorship came to me when I decided to start moving to [Pixiv](https://www.pixiv.net/en/). I checked their rules and came across ones that require artists to censor genitals in their works, according to Japanese law (specifically, the infamous Article 175 of the Japanese Criminal Code). I'm against censorship, but if I want to upload my explicit works to the site, I have to obey the rules.

As an unorthodox compromise (after all I can always just share links to uncensored works variants, duh), I came up with solutions of modifying images in the ways that severely distort the specified "obscene" region, alike to black bars and pixelization ("mosaics"). Unlike the black bars and pixelization, which are irreversibly destroying the original image information, mine methods are only modifying it in a way that may be reverted to the original, uncensored image.

My methods are essentially the combination of primitive cryptography and steganography: the specified area of the image is being encrypted, and then an additional hidden information ("the key") in being added to the censored image for further automatic uncensoring (decryption of the distorted area, restoring to the original).

## Methods
There are 3 available methods of reversible censorship, which can be combined. Although, using just one is enough to conceal the specified area.

The PNG images below will be used for demonstrating the censorship methods. Pixel art one will be used in the orignal (small) resolution and upscaled after the transformation.
> [Handholding original source](https://x.com/suzuha00/status/1870830462266167516). [Silly pixel art meme by me](https://www.newgrounds.com/art/view/redreaperripper/so-true-bestie-pegs-you).

![original](https://github.com/user-attachments/assets/16eeda68-eab8-43be-8b58-a7093714b30f)
![original_x4](https://github.com/user-attachments/assets/b3ec8a02-23ee-45e7-986f-adf322618ff5)
![original](https://github.com/user-attachments/assets/01d2d195-0fef-4470-b906-21eacb19f6fc)

> `1st` image region specification: [120](a "X position (from left)") [267](a "Y position (from top)") [92](a "Width (X size, to right)") [121](a "Height (Y size, to down)")
>
> `2nd` image region specification: 85 78 16 21

### "Mixing" method
This method changes the order of pixels in the specified area by transposing it 5 times, turning the region into a unified mess.

> [!CAUTION]
> The specified area should not be a perfect square, otherwise this method won't distort the area as intended.

![censored](https://github.com/user-attachments/assets/59e29856-3cc4-4b50-9c2d-cd8df63ac272)
![censored](https://github.com/user-attachments/assets/32637ed1-7ad1-45d0-9139-3eb1effbdf0f)

### "Noising" method
This method adds a certain value to the color value according to the formula (takes pixel X and Y positions as arguments) and then performs modulo operation by 256. To additionally distort the specified region, a hue shift is being performed by swapping the color channels: R→G, G→B, B→R.

![censored](https://github.com/user-attachments/assets/0597f94d-e831-4643-854b-027a4c5048a5)
![censored](https://github.com/user-attachments/assets/7818b770-4863-454c-b2df-f0b51bfd26a5)

### "Hiding" method
This method just sets the alpha channel value of the specified area's pixels to 0, making the area fully transparent, yet still containing the color data.

> [!CAUTION]
> The specified area should not have transparent or semi-transparent pixels, otherwise this method will essentially corrupt the image, since there's no way to restore the original opacity level.

![censored](https://github.com/user-attachments/assets/376b1815-d417-4054-be05-624a04284bf0)
![censored](https://github.com/user-attachments/assets/844dd195-6617-49dd-96a1-c9a9a4665a89)

### Combining methods
Methods can be combined to scramble the specified area even further. Here is the result of using both the "mixing" and the "noising":

![censored](https://github.com/user-attachments/assets/b62ef1e8-cd0d-44dc-82ae-1817c5775fea)
![censored](https://github.com/user-attachments/assets/5bf180a9-8b91-4440-81bd-e5b6771f4e91)

## Additional data hiding
When censoring the image, the last row of the image is being copied and added to the output image, this way increasing the image's height by 1 pixel. Into this additional row, a data necessary for automatic uncensoring is being injected. The information is being stored 1 bit per pixel, in the last bit of the blue channel.

The structure of the data row is such (from right to left)
| Pixels | Data |
| ----------- | ----------- |
| 2 | [Scale mark](a "The first pixel contains 0, the second pixel contains 1. In case if the censored image will be upscaled by some integer number (pixel art upscaling, for example), the tool will detect it and still correctly uncensor the image.") |
| 16 | Position X |
| 16 | Position Y |
| 16 | Size X |
| 16 | Size Y |
| 3 | Methods flags |

**Total:** 69 pixels. In this way, the original image should be at least that wide so it can be censored.

## Instruction
For censoring:
1. Place an original PNG image into the directory with `main.py` as `original.png`
2. Run `main.py`
3. Enter 2
4. Enter 4 numbers separated with space: X position, Y position, X size, Y size
5. Enter a combination of three 1s and 0s separated with space to determine which methods to use
6. A `censored.png` image will appear in the same directory

For uncensoring:
1. Place a PNG image censored with this tool into the directory with `main.py` as `censored.png`
2. Run `main.py`
3. Enter 1
4. ???
5. PROFIT! Now `uncensored.png` should appear in the same dir

## Afterword
I want to say thank you to people from Discord who gave me some hints on this tool implementation.
- "Noising" method (hue shift part): @unitrader
- "Hiding" method: @74363, @unitrader
- "Mixing" method: @reverse_mitts
- Additional data row: @tasadar2, @74363, @unitrader
