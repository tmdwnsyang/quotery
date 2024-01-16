import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import collections


def get_quotes_from_pages():
    print('Reaching https://quotes.toscrape.com/...')
    base_url = "https://quotes.toscrape.com/"
    url = base_url + "/page/1"  # first page of quotes
    page = requests.get(url, timeout=60)
    soup = BeautifulSoup(page.content, 'html.parser')

    quotes = []

    # iterate through all the pages of quotes and collect the quotes
    print('Iterating each page for appropriate attributes for relevant quotes...')
    while True:
        quotes_on_page = soup.find_all('div', attrs={'class': 'quote'})
        quotes.extend(quotes_on_page)

        next_page = soup.find('li', class_='next')
        if next_page:
            url = base_url + next_page.a['href']
            page = requests.get(url, timeout=60)
            soup = BeautifulSoup(page.content, 'html.parser')
        else:
            break
    print('done!')
    return quotes

# get the most common tags in the site


def find_most_common_tags(quotes):
    print('Fetching tags and sorting by frequencies...')
    # quotes = get_quotes_from_pages()

    tag_freq = {}

    for quote in quotes:
        tags = quote.find_all('a', href=True, attrs={'class': 'tag'})
        for tag in tags:
            if tag.text in tag_freq:
                tag_freq[tag.text] += 1
            else:
                tag_freq[tag.text] = 1

    print("Most common tags: ")
    for tag, freq in sorted(tag_freq.items(), key=lambda x: x[1], reverse=True):
        print(tag, freq)

    # plot the top 15 frequencies
    sorted_tags = sorted(
        tag_freq.items(), key=lambda x: x[1], reverse=True)[:15]
    tags = [tag for (tag, _) in sorted_tags]
    frequencies = [freq for (_, freq) in sorted_tags]

    plt.bar(tags, frequencies)
    plt.xlabel('Tag')
    plt.ylabel('Frequency')
    plt.title('Top 15 Tag Frequencies')
    plt.xticks(rotation=90)
    plt.show()

def printDash(l):
    [print('-',end='') for c in l]
    print()

# takes in an author's name as a paratemeters and returns the tags associated with them
def list_quote_types_by_author(quotes):

    # quotes = get_quotes_from_pages()
    quotes_by_author_dict = collections.defaultdict(list)

    # For each quote...
    for quote in quotes:
        # Gathering author name
        author_name = quote.find('small', class_='author').get_text()
        # Gathering all relevant tags
        rel_tags = [tags.get_text() for tags in quote.find(
            'div', {'class': 'tags'}).findAll('a', recursive=False)]
        # Placing (author name, tags) in tupples and adding to dict.
        quotes_by_author_dict[author_name].append(
            (quote.find('span', class_='text').get_text(), rel_tags))
    [print("> " + names) for names in quotes_by_author_dict.keys()]

    print("Please enter the author's name to display all relevant quotes followed by relevant tags: ")
    user_author = input()
    while True:
        if (user_author == 'menu'):
            break
        if (user_author not in quotes_by_author_dict.keys()):
            print('There are no quotes by this author. Please choose another:')
        else:
            printDash(user_author)

            for (quote, tags) in quotes_by_author_dict[user_author]:
                print(quote)
                for tag in tags:
                    print(' |_' + tag)
            printDash(user_author)
            print(
                'Please enter another author name to view more. Otherwise, type "menu".')
        user_author = input()


# takes in a tag as a parameter and returns the quotes associated with that tag
def search_quotes_by_tag(quotes):
    # quotes = get_quotes_from_pages()
    tag_quote_dict = collections.defaultdict(list)
    for quote in quotes:
        tags = [tags.get_text() for tags in quote.find(
            'div', {'class': 'tags'}).findAll('a', recursive=False)]
        for t in tags:
            tag_quote_dict[t].append(quote.find(
                'span', class_='text').get_text())

    [print('> ', x) for x in tag_quote_dict.keys()]
    print("Please select a tag from the above. Type 'menu' to go to options. ")
    
    user_tag = input().lower()
    while True:
        if (user_tag == 'menu'):
            print('Exiting application...')
            return
        if (user_tag not in tag_quote_dict.keys()):
            print("Please choose a valid tag!")
        else:
            printDash(user_tag)
            [print(q) for q in tag_quote_dict[user_tag]]
            printDash(user_tag)

            print('Please select a tag. Otherwise, please enter \'menu\'')
        user_tag = input().lower()


def main():
    # get most common tags across all quotes
    quotes = get_quotes_from_pages()

    while True:
        print("Select from the following options:")
        print(" 1. Search quotes by tag.")
        print(" 2. Search quotes by author and display relevant tags.")
        print(" 3. Display most common tags.")
        print(" 4. Exit.")

        user_choice = input().lower()
        match user_choice:
            case "1":
                search_quotes_by_tag(quotes)
            case "2":
                list_quote_types_by_author(quotes)
            case "3":
                find_most_common_tags(quotes)
            case "4":
                print("Exiting...")
                return
            case _:
                print("Invalid input!")


main()
# call the function for the simple search engine
