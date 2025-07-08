Let's create the full end-to-end actionable project design and build for this open-source public art project!

* It will run on a raspberry pi 5
* Kiosk full-screen mode
* Single display 1024 x 600 pixel touchscreen
* Landscape orientation
* No user text entry

This art project explores the limitations of demographic survey forms and the biases of AI image generation. A user uses the touch screen to fill out basic demographic form selections, and the display calls an image generation API to generate photographic-style portrait images. (The image generation is rapid, about 3 or 4 seconds, so the interface should always try to update in response to form selection changes, rather than wait for a submission / generation request; no "submit" button needed.)

The demographics form fields will appear on the right side of the landscape screen. The most-recently-generated AI image will appear on the left side of the landscape sceen, with the associated form-selected values used to generate the image. At program launch, there will be a placeholder image shown. This image is 512x512 pixels, the nominal typical image size for this project, and is located at `ui_elements/unknown_portrait.png`. When this startup image is displayed, all of the demographic category values will show question mark `?`.

The application will have config variables for image generation prompt prepended text, appended text, and "negative prompt" text. The user-selected form values will, in some cases, be mapped to associated strings better-suited to image generation prompts, and recrafted into stable diffusion syntax, which may include comma separators, (parentheses) for intensification, and [brackets] for reduction of intensity of a given term, as configured.

Other image generation settings will also be developer-configurable.

The image generation API may include authentication secrets.

