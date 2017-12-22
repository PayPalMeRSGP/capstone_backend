# capstone_backend
- GET [base_url]/everything
    
    returns every asset in s3, use when user first installs app in JSON format. Upload time is a LONG representating unix time.

    documentation:
    ```json
    {
        "<gallery_title>": [
            {
                "asset_url": "<url to gallery asset in amazon s3, can be an image, video, GIF, etc.>",
                "text": "<corresponding decription of the asset found under the asset_url>",
                "upload_time": 123456789
            }
        ]
    }
    ```

    example:
    ```json
    {
        "example_slideshow": [
            {
                "asset_url": "http://psyche-andromeda.s3.amazonaws.com/example_slideshow/asteroid.jpg",
                "text": "This is an image of the psyche asteroid. And this is a test message.",
                "upload_time": 1513932972
            },
            {
                "asset_url": "http://psyche-andromeda.s3.amazonaws.com/example_slideshow/bitcoin.jpg",
                "text": "This is an image of bitcoins being sucked into a black hole. And this is a test message. ",
                "upload_time": 1513933519
            },
            {
                "asset_url": "http://psyche-andromeda.s3.amazonaws.com/example_slideshow/album.jpg",
                "text": "This is an image of a record album presumably named \"Andromeda\". There are also 3 suns with faces on them, they are positioned to the left, center and right.\r\nThe ones on the left and right are only partialy shown. And this is a test message. ",
                "upload_time": 1513938099
            }
        ]
    }
    ```

-GET [base_url]/filter?=[unix_timestamp]

returns everything uploaded after the GET parameter, to be used when polling for any gallery updates. It is up the the client app to     store their own last upload unix_timestamp.

documentation: same format as GET [base_url]/everything
