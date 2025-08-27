from weasyprint import HTML


class Tabler:
    def __init__(self):
        with open("ressources/toggable_calendar.html", "r") as file:
            self.html_content = file.readlines()

    def fill_cell(self, day: int, hour: int, content):
        print(f"day: {day}, hour: {hour}, content: {content}")
        comment = f"    <!-- {hour}h -->\n"
        print(f"comment is {comment}")
        index = self.html_content.index(comment) + day
        text = f'    <div class="filling">{content}</div>'
        self.html_content[index] = text

    def save_pdf(self, path):
        text = "".join(self.html_content)
        HTML(string=text).write_pdf(path)
