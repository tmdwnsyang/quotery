import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import collections


def get_quotes_from_pages():
    print('Reaching https://quotes.toscrape.com/...')
    base_url = "https://quotes.toscrape.com/"
    url = base_url + "/page/1"  # first page of quotes
    page = requests.get(url)
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
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
        else:
            break
    print('done!')
    return quotes

# get the most common tags in the site


def find_most_common_tags():
    print('Fetching tags and sorting by frequencies...')
    quotes = get_quotes_from_pages()

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

# takes in an author's name as a paratemeters and returns the tags associated with them


def list_quote_types_by_author():

    quotes = get_quotes_from_pages()
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
    famous_author = input()
    while True:
        if (famous_author == 'next'):
            break
        if (famous_author not in quotes_by_author_dict.keys()):
            print('There are no quotes by this author. Please choose another:')
        else:
            for (quote, tags) in quotes_by_author_dict[author_name]:
                print('> ' + quote)
                for tag in tags:
                    print(' |_'+ tag)
            print('Please enter a another author name to view more. Otherwise, type "next".')
        famous_author = input()


# takes in a tag as a parameter and returns the quotes associated with that tag
def search_quotes_by_tag(tag):
    quotes = get_quotes_from_pages()
    found_quotes = []

    for quote in quotes:
        tags = quote.find_all('a', href=True, attrs={'class': 'tag'})
        for quote_tag in tags:
            if quote_tag.text.lower() == tag.lower():
                quote_text = quote.find('span', class_='text').text.strip()
                found_quotes.append(quote_text)

    return found_quotes


def main():
    # get most common tags across all quotes
    find_most_common_tags()

    list_quote_types_by_author()

    l = set()
    quotes = get_quotes_from_pages()
    for quote in quotes:
        tags = quote.find_all('a', href=True, attrs={'class': 'tag'})
        for tag in tags:
            l.add(tag.text.lower())

    for x in l:
        print('> ', x)
    print("Please select a tag from the above. Type 'exit' to exit. ")

    user_input = input().lower()
    while True:
        if (user_input == 'exit'):
            print('Exiting application...')
            return
        if (user_input not in l):
            print("Please choose a valid tag!")

        else:
            quotes_with_tag = search_quotes_by_tag(user_input)
            for quote in quotes_with_tag:
                print(quote, '\n')
            print('Please select a tag. Otherwise, please enter \'exit\'')
        user_input = input().lower()


main()
# call the function for the simple search engine
