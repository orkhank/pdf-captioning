import textwrap

# The prompts are used to generate captions for images
# The prompts are taken from this paper: https://arxiv.org/abs/2406.10328v1
_RAW_PROMPTS = [
    """
    Describe the image in detail. Please specify any objects within the
    image, backgrounds, scenery, interactions, and gestures or poses.
    If they are multiple of any object, please specify how many and where
    they are. If any text is present in the image, mention where it is,
    and the font. Describe the text in detail with quotation marks.
    For example, if the image has text, Merry Christmas, write it down as
    "Merry Christmas". Describe the style of the image. If there are people
    or characters in the image, what emotions are they conveying?
    Identify the style of the image, and describe it as well.
    Please keep your descriptions factual and terse but complete.
    The description should be purely factual, with no subjective
    speculation. Make sure to include the style of the image, for example
    cartoon, photograph, 3d render etc.
    Start with the words 'This image displays:'
    """,
    """
    Describe every component of this image, as it were described by an artist
    in atmost two paragraphs. Each object, with its count, positions, and
    attributes should be described. Describe the text, and the font in detail
    with its contents in quotation marks. For example if the image has text
    Happy Birthday, write it down as "Happy Birthday". Include the style of
    the image for example photograph, 3d-render, shopping website etc. Capture
    the aesthetics of the image, as if described by an artist.
    Start with the words 'This image displays:'
    """,
    """
    Describe the image, the foreground and the background. All objects, along
    with its count and positions must be described. For any text present in
    the image, describe the text using quotation marks. Be factual in your
    description, capturing the content, and style of the image. Describe the
    image, in a short but desciptive manner.
    Start with the words 'This image displays:'
    """,
    """
    Write a detailed caption describing the image. Include all components, and
    objects with their positions. If any text is present in the image, and
    describe the text contents in quotation marks. For example if the image
    has text Happy Birthday, write it down as "Happy Birthday". Be detailed in
    your description of the image, and write as if it were being described by
    a boring person. Start with the words 'This image displays:'
    """,
    """
    Don't forget these rules:
    1. Be Direct and Concise: Provide straightforward descriptions without
    adding interpretative or speculative elements.
    2. Use Segmented Details: Break down details about different elements of
    an image into distinct sentences, focusing on one aspect at a time.
    3. Maintain a Descriptive Focus: Prioritize purely visible elements of the
    image, avoiding conclusions or inferences.
    4. Follow a Logical Structure: Begin with the central figure or subject
    and expand outward, detailing its appearance before addressing the
    surrounding setting.
    5. Avoid Juxtaposition: Do not use comparison or contrast language; keep
    the description purely factual.
    6. Incorporate Specificity: Mention age, gender, race, and specific brands
    or notable features when present, and clearly identify the medium if it's
    discernible. When writing descriptions, prioritize clarity and direct
    observation over embellishment or interpretation.
    Write a detailed description of this image, do not forget about the texts
    on it if they exist. Also, do not forget to mention the type/style
    of the image. No bullet points.
    Start with the words, "This image displays:"
    """,
]

# Remove newlines and leading/trailing whitespace
PROMPTS = [
    textwrap.dedent(prompt).replace("\n", " ").strip()
    for prompt in _RAW_PROMPTS
]


def main():
    """Prints the processed prompts to the console."""
    fill_width = 80

    print("Prompts:")
    for prompt in PROMPTS:
        print("-" * fill_width)
        print(textwrap.fill(prompt, width=fill_width))


if __name__ == "__main__":
    main()
