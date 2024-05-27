import urllib.parse
import sass  # type: ignore
import json5


def generate_scss(
    channel_id: str,
    svg_icon: str,
    channel_name: str,
    mute_icon: str,
    color: str = "#BDBDBD",
    template: str = "",
) -> str:
    if not color.startswith("#") and len(color) in (3, 6):
        color = f"#{color}"
    encoded_svg = urllib.parse.quote(svg_icon)
    encoded_svg_mute = urllib.parse.quote(mute_icon)
    scss_code = (
        template.replace("<id>", channel_id)
        .replace("<svg>", encoded_svg)
        .replace("<name>", channel_name)
        .replace("<color>", color)
        .replace("<mute>", encoded_svg_mute)
    )
    return scss_code


def append_to_file(file_path, content):
    with open(file_path, "a") as file:
        file.write(content)


def read_file(file_path):
    with open(file_path, "r") as file:
        return file.read()


def compile_scss_to_css(scss_code):
    return sass.compile(string=scss_code)


def write_file(file_path, content):
    with open(file_path, "w") as f:
        f.write(content)


generate_dict = {}
with open("./generate.jsonc") as f:
    generate_dict = json5.load(f)

with open("./theme.scss", "w") as f:
    f.write("")

with open("./default.scss", "r") as f:
    append_to_file("./theme.scss", f.read())

for x in generate_dict["channels"]:
    with open(x["svg"]) as f:
        svg_str = f.read()
    with open(generate_dict["settings"]["mute_icon"]) as f:
        svg_str_mute = f.read()

    color = "#BDBDBD"
    if "color" in x:
        color = x["color"]
    template = "./template.scss"
    noname_template = "./template-noname.scss"
    name_template = "./template-name.scss"
    with open(template) as f:
        template = f.read()
    if "name" not in x:
        x["name"] = ""
        with open(noname_template) as f:
            template += f.read()
    else:
        with open(name_template) as f:
            template += f.read()
    scss = generate_scss(
        channel_id=str(x["id"]),
        svg_icon=svg_str,
        channel_name=x["name"],
        color=color,
        template=template,
        mute_icon=svg_str_mute,
    )
    append_to_file("./theme.scss", scss)
    scss_file_content = read_file("./theme.scss")
    compiled_scss = compile_scss_to_css(scss_file_content)
    write_file("./theme.css", compiled_scss)
