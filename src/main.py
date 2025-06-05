from markdowntohtml import *

def main():
    a = TextNode("achor text", TextType.LINK, "https://www.google.com")
    b = TextNode("bold text", TextType.BOLD)

    print(a)
    print(b)

if __name__ == "__main__":
    main()