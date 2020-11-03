# Media queries i responsivni dizajn - vježba

U ovoj jednostavnoj vježbi responsivnog dizajna ćete proći nekoliko koraka:
1. Stvoriti osnovnu HTML datoteku s par CSS pravila kojima bojamo različite dijelove stranice.
2. Zatim ćemo dodati media queries koji će na širim ekranima (_40em_) navigacijsku traku i članak raširiti horizontalno.
3. Dodat ćemo još jedan uvjet koji će i poslednji dio stranice prikazati sa strane kad je širina veća od _70em_.

## Korak 1
Kreirajte HTML početnu datoteku sa slijedećim sadržajem:

```html

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Media Queries: a simple mobile first design, step 1</title>
    <meta name="viewport" content="width=device-width">
    <style>
      * {
        box-sizing: border-box;
      }

      body {
        width: 90%;
        margin: 2em auto;
        font: 1em/1.3 Arial, Helvetica, sans-serif;
      }

      a:link,
      a:visited {
        color: #333;
      }

      nav ul,
      aside ul {
        list-style: none;
        padding: 0;
      }

      nav a:link,
      nav a:visited {
        background-color: rgba(207, 232, 220, 0.2);
        border: 2px solid rgb(79, 185, 227);
        text-decoration: none;
        display: block;
        padding: 10px;
        color: #333;
        font-weight: bold;
      }

      nav a:hover {
        background-color: rgba(207, 232, 220, 0.7);
      }

      .related {
        background-color: rgba(79, 185, 227, 0.3);
        border: 1px solid rgb(79, 185, 227);
        padding: 10px;
      }

      .sidebar {
        background-color: rgba(207, 232, 220, 0.5);
        padding: 10px;
      }

      article {
        margin-bottom: 1em;
      }

    </style>
  </head>

  <body>
    <div class="wrapper">
      <header>
        <nav>
          <ul>
            <li><a href="">O stranici</a></li>
            <li><a href="">Kontakt</a></li>
            <li><a href="">Naš tim</a></li>
            <li><a href="">Blog</a></li>
          </ul>
        </nav>
      </header>
      <main>
        <article>
          <div class="content">
            <h1>Povrće!</h1>
            <p>
              Veggies es bonus vobis, proinde vos postulo essum magis kohlrabi
              welsh onion daikon amaranth tatsoi tomatillo melon azuki bean
              garlic.
            </p>
            <p>
              Gumbo beet greens corn soko endive gumbo gourd. Parsley shallot
              courgette tatsoi pea sprouts fava bean collard greens dandelion
              okra wakame tomato. Dandelion cucumber earthnut pea peanut soko
              zucchini.
            </p>
            <p>
              Turnip greens yarrow ricebean rutabaga endive cauliflower sea
              lettuce kohlrabi amaranth water spinach avocado daikon napa
              cabbage asparagus winter purslane kale. Celery potato scallion
              desert raisin horseradish spinach carrot soko. Lotus root water
              spinach fennel kombu maize bamboo shoot green bean swiss chard
              seakale pumpkin onion chickpea gram corn pea. Brussels sprout
              coriander water chestnut gourd swiss chard wakame kohlrabi
              beetroot carrot watercress. Corn amaranth salsify bunya nuts nori
              azuki bean chickweed potato bell pepper artichoke.
            </p>
            <p>
              Nori grape silver beet broccoli kombu beet greens fava bean potato
              quandong celery. Bunya nuts black-eyed pea prairie turnip leek
              lentil turnip greens parsnip. Sea lettuce lettuce water chestnut
              eggplant winter purslane fennel azuki bean earthnut pea sierra
              leone bologi leek soko chicory celtuce parsley jícama salsify.
            </p>
          </div>
          <aside class="related">
            <p>
              Latinski tekst o povrću je generiran pomoću
              <a href="https://veggieipsum.com/">Veggie Ipsum generatora</a>.
            </p>
          </aside>
        </article>

        <aside class="sidebar">
          <h2>Neki linkovi o povrću</h2>
          <ul>
            <li>
              <a href="https://www.coolinarika.com/namirnica/brokula/">Kako pripremiti brokule</a>
            </li>
            <li>
              <a href="https://www.vrtlarica.hr/sadnja-uzgoj-blitve/">Sadnja i uzgoj blitve</a>
            </li>
            <li>
              <a href="http://www.batat.hr/">Batat - slatki krumpir</a>
            </li>
          </ul>
        </aside>
      </main>

      <footer><p>&copy;2020</p></footer>
    </div>
  </body>
</html>
```

Stranicu snimite i pregledajte u Dev Tools kako izgleda u nekom mobilnom pregledniku.

## Korak 2
Zatim ćemo navigacijsku traku i članak (_article_) uz pomoć media queries učiniti da na širim rezolucijama uzimaju više horizontalnog prostora. Dodajte u CSS:

```css
@media screen and (min-width: 40em) {
    article {
        display: grid;
        grid-template-columns: 3fr 1fr;
        column-gap: 20px;
    }

    nav ul {
        display: flex;
    }

    nav li {
        flex: 1;
    }
}
```
Osvježite stranicu i pogledajte njeno ponašanje na užim i širim rezolucijama.

## Korak 3
Dodajte još sljedeći CSS kod koji će cijelu stranicu oblikovati kao _flex grid_ u slučaju ako je širina preglednika veća od _70em_. Također ćemo ukloniti donju marginu članka, a podnožju ćemo dodati gornju stranicu okvira:

```css
@media screen and (min-width: 70em) {
    main {
        display: grid;
        grid-template-columns: 3fr 1fr;
        column-gap: 20px;
    }

    article {
        margin-bottom: 0;
    }

    footer {
        border-top: 1px solid #ccc;
        margin-top: 2em;
    }
}
```

Ponovo snimite i osvježite stranicu i pogledajte njeno ponašanje na užoj, srednjoj i najširoj rezoluciji. Vidimo da stranica ovisno o širini poprima oblik s jednom, dvije ili tri kolone.

Ovo je promjer jednostavnog responsivnog dizajna.

[🏠 Početna](../../.) | [📃 Povratak](../.)
