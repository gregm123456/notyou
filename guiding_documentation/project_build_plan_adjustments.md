Fine-tuning notes and adjustments required for project build plan:

# automatic1111 stable diffusion api authentication:

* The image generation service will be launched with `--api-auth	API_AUTH		Set authentication for API like username:password`; this project will store the username and password in the project secrets file, which will be in .gitignore.
* the request structure in python is `requests.post(url=f'{URL}/sdapi/v1/txt2img', json=payload, auth=('username', 'password'))`

# form requirements and image generation responsiveness

* As soon as a first form field value is selected, the image generation is invoked.
* Any change to any field value selection will invoke a new image generation.
* No single field is required; as soon as one or more fields have been assigned a value by the user, an image will be generated.
* In the case of rapid form changes, each new change moves to the front of the queue; any previously-queued unfulfilled image generations that have not been completed will be abandoned and never sent to the image generation api.

# demographic fields

The project build plan was created with reasonable demographics fields and values, but, since this art project is meant to explore biases, we will represent demographics with this more-traditional field/value set:

1. **Age**: Child, Teen, Young Adult, Middle-Aged, Senior
2. **Gender**: Male, Female
3. **Ethnicity**: White, Asian, American Indian, Black or African American, Hispanic Latino or Spanish origin, Middle Eastern or North African, Native Hawaiian or Other Pacific Islander, Other
4. **Education**: Some schooling, high school, college, graduate / professional degree
5. **Employment status**: Unemployed, student, part-time, full-time, retired
6. **Income**: $0–$24,999, $25,000–$49,999, $50,000–$99,999, $100,000–$199,999, $200,000+

Note that each field will have an empty/unselected/unset value choice, as no field is required.