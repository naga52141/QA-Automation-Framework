def test_footer_social_links(inventory_page):

    links = inventory_page.get_footer_social_links()

    assert any("twitter.com" in link for link in links)
    assert any("facebook.com" in link for link in links)
    assert any("linkedin.com" in link for link in links)
