import os


def read_link(path):
    file = open(path, 'r')

    while True:
        line = file.readline()

        # Ignore blank lines
        if line == '\n':
            continue

        # End of file
        if line == '':
            break

        # Ignore coments
        if line.startswith('#'):
            continue

        link = line

    if link.endswith('\n'):
        link = link[:-1]
    return link


html_body = """<!DOCTYPE html>
<html lang="es">
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>| Radios</title>
        
        <!-- Bootstrap CSS -->
        <link rel="stylesheet" href="./bootstrap-3.3.7-dist/css/bootstrap.min.css">
        <!-- Personal CSS -->
        <link rel="stylesheet" href="./css/main.css">
        <!-- Jquerry -->
        <script src="https://code.jquery.com/jquery-3.1.1.min.js"></script>
    </head>

    <body>
        <div class="streaming">
            <audio id="streamingControls" src="http://94.23.40.42:8046/;stream.aac" controls="controls" preload="none">
            </audio>
        </div>
        
        <div class="container">
        {0}
        </div><!--/container -->
        
        <footer id="footer">
          <h2 class="header-hidden">Footer</h2>

          <div class="footer section">
            <div class="container" style="padding-top: 30px;">
              <div class="footer-texto">

            <a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.

            <p></> with <i class="fa fa-heart" aria-hidden="true"></i> by <a href="http://twitter.com/fnbellomo" target="_blank">@fnbellomo</a></p>
              </div><!--/footer-texto -->

            </div><!--/container -->
          </div><!--/footer section-->
        </footer>
        
        <script>
            var audio = document.getElementById("streamingControls");
            audio.addEventListener('error', function failed(e) {{
               // audio playback failed - show a message saying why
               // to get the source of the audio element use $(this).src
               switch (e.target.error.code) {{
                 case e.target.error.MEDIA_ERR_ABORTED:
                   alert('You aborted the video playback.');
                   break;
                 case e.target.error.MEDIA_ERR_NETWORK:
                   alert('A network error caused the audio download to fail.');
                   break;
                 case e.target.error.MEDIA_ERR_DECODE:
                   alert('The audio playback was aborted due to a corruption problem or because the video used features your browser did not support.');
                   break;
                 case e.target.error.MEDIA_ERR_SRC_NOT_SUPPORTED:
                   alert('The video audio not be loaded, either because the server or network failed or because the format is not supported.');
                   break;
                 default:
                   alert('An unknown error occurred.');
                   break;
               }}
             }}, true);
        
            var oldRadio = "";

            function playRadio(streaming, radioName) {{
                // Update the page title with the radio name
                document.title = radioName + " | Radios";

                // Play the radio
                var audio = document.getElementById("streamingControls");
                audio.src = streaming;
                audio.play();
                
                // Add img-active class
                var image = document.getElementById(radioName);
                image.className = "img-responsive box-img img-active";
              
                // Remove img-active class to old radio play
                if (oldRadio) {{
                    var image = document.getElementById(oldRadio);
                    image.className = "img-responsive box-img";
                }}
                oldRadio = radioName;
            }}
        </script>
    </body>
</html>
"""

col = """
<div class="col-xs-6 col-sm-3 col-md-3">
    {0}
</div><!--/col-sm-3 -->
"""

radio_div = """<div class="box">
    <img id="{1}" src="./{0}" class="img-responsive box-img" alt="radio {1}" onclick="playRadio('{2}', '{1}')" />
</div><!--/box -->
"""

# Get all source and image files
files = os.listdir('./')
links_files = [file for file in files if file.endswith('.m3u')]
images = [file for file in files if file.endswith('.tbn')]

links_files.sort()
images.sort()

streamings = [read_link('./' + link) for link in links_files]

divs = []
for image, streaming in zip(images, streamings):

    if streaming.startswith('http'):
        text = radio_div.format(image, image[:-4], streaming)
        divs.append(text)

rows = ''
for cnt, div in enumerate(divs):
    if cnt == 0:
        rows += '<div class="row">'
    elif cnt % 4 == 0:
        rows += '</div><!--/row -->'
        rows += '<div class="row">'

    rows += col.format(div)

    if cnt == len(divs):
        rows += '</div><!--/row -->'

# Save the html to file
html = html_body.format(rows)

with open('index.html', 'w') as file:
    for line in html:
        file.write(line)
