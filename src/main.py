from textnode import *

def main():
    a = TextNode("achor text", TextType.LINK_TEXT, "https://www.google.com")
    b = TextNode("bold text", TextType.BOLD_TEXT)

    print(a)
    print(b)

if __name__ == "__main__":
    main()