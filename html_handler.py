import os.path

def append_div(author_url, username, body_text, filename):
    global base_file
    if os.path.exists(filename) == False:
        return None

    p_tag = "<p>"
    p_tag += str(body_text)
    p_tag += "</p>"

    h_tag = "<p class=\"username\">"
    h_tag += str(username)
    h_tag += "</p><br>"

    img_tag = "<img src={} class=\"avatar\"></img>".format(author_url)
    
    container_div = "<div>"
    container_div += img_tag
    container_div += h_tag
    container_div += p_tag
    container_div += "</div>"

    with open(str(filename), "a") as output_file:
        output_file.write(container_div)
        print("message added")

def generate_html(filename):
    with open(str(filename), "a") as output_file:
        output_file.write("</body></html>")