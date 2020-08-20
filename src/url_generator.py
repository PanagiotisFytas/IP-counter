import ipaddress


def generate_ip_addresses(number_of_addr: int):
    """
    :param number_of_addr: the number of unique ip adresses to generate
    :return a list of unique ip addresses
    """
    base_ip = ipaddress.ip_address('0.0.0.0')
    addresses = []
    for idx in range(number_of_addr):
        addresses.append(str(base_ip + idx))
    return addresses

def generate_post_options(post_endpoint: str, ip_list: list):
    """
    :param post_endpoint: the endpoint url for post calls (e.g. http://localhost:5000/logs)
    :param ip_list:
    :return a list of posts usable by siege
    """
    posts = []
    for ip in ip_list:
        # format into a post url useable by siege
        post = post_endpoint + " POST {{\"timestamp\": \"dummytimestamp\", \"ip\": \"{}\", \"url\": \"dummyurl\"}}".format(ip)
        posts.append(post)
    return posts

if __name__ == "__main__":

    base_url = 'http://localhost:5000'

    number_of_requests = 1000000

    # get_endpoint = base_url + '/visitors'
    post_endpoint = base_url + '/logs'
    # generate different ip addresses
    ip_addresses = generate_ip_addresses(number_of_requests)

    # print them
    urls = generate_post_options(post_endpoint, ip_addresses)
    for url in urls:
        print(url)