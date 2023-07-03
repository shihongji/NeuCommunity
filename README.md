# NeuCommunity - NEU Hackers
A project for builder's dojo. The product is a community that let users ask and share solutions.

Here is the presentation deck that introduces the product in detail. 

[Presentation Deck](Builders_Dojo_Presentation_Hongji%26Yang_202303_v1.pdf)

## How to run this project on your local machine?
1. Clone this repo
2. Create your Python virtual environment and activate it
 - use the following command to create and activate virtual environment named `.venv`
    ```
    # Linux
    sudo apt-get install python3-venv    # If needed
    python3 -m venv .venv
    source .venv/bin/activate

    # macOS
    python3 -m venv .venv
        source .venv/bin/activate

    # Windows
    py -3 -m venv .venv
    .venv\scripts\activate
    ```

4. Install the packages in `requirements.txt`,

    `pip3 install -r requirements.txt`
5. `python3 manage.py migrate`
Then you could run server by `python3 manage.py runserver`.


