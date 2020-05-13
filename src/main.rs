use fantoccini::{Client, Locator};
use reqwest;
use std::fs::File;

// let's set up the sequence of steps we want the browser to take
#[tokio::main]
async fn main() -> Result<(), fantoccini::error::CmdError> {
    let mut c = Client::new("http://localhost:4444")
        .await
        .expect("failed to connect to WebDriver");

    // first, go to the Wikipedia page for Foobar
    c.goto("https://cooking.nytimes.com").await?;
    let url = c.current_url().await?;
    assert_eq!(url.as_ref(), "https://cooking.nytimes.com/");

    c.wait_for_find(Locator::Css(".nytc---loginbtn---loginBtn"))
        .await?;

    // click "Foo (disambiguation)"
    c.find(Locator::Css(".nytc---loginbtn---loginBtn"))
        .await?
        .click()
        .await?;
    while let Ok(_) = c
        .find(Locator::XPath(
            r#"//iframe[@title="Log in and Registration"]"#,
        ))
        .await
    {}

    // Basically the same selector for "YOUR RECIPE BOX" as for "Log in"
    c.wait_for_find(Locator::Css(".nytc---loginbtn---loginHover"))
        .await?;

    // click "Foo (disambiguation)"
    c.find(Locator::Css(".nytc---loginbtn---loginHover"))
        .await?
        .click()
        .await?;

    c.wait_for_find(Locator::LinkText("Saved Recipes")).await?;

    c.find(Locator::LinkText("Saved Recipes"))
        .await?
        .click()
        .await?;

    c.wait_for_find(Locator::Css("article")).await?;

    let mut articles = Vec::new();
    let mut content = String::new();
    for mut article in c.find_all(Locator::Css("article")).await? {
        let link = article
            .find(Locator::Css(".nytc---cardbase---linkWithImage"))
            .await?
            .attr("href")
            .await?;
        if let Some(val) = link {
            content.push_str(&format!("{}\n", val));
            articles.push(val);
        }
    }

    c.close().await?;

    use std::io::Write;
    let mut file = File::create("links.txt").unwrap();
    file.write_all(content.as_bytes()).unwrap();

    Ok(())
}
