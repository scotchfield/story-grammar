# story-grammar
A grammar for generating stories, inspired by [NaNoGenMo 2016](https://github.com/NaNoGenMo/2016/).

## Getting Started
You can start using the story grammar scripts immediately. Feel free to clone the repository, and run `python parser.py <input_filename>`.

For example,

    git clone https://github.com/scotchfield/story-grammar.git
    cd story-grammar
    python parser.py stories/simple.txt

You should see something like this:

    Starting rule: ['Story']
    Setting Protagonist (Names) to value Laura
    Setting ProtagonistAdjective (Adjectives) to value scary
    Once upon a time, there was a hero named Laura. Laura was a scary fighter. Then Laura went for a scary walk. And Laura died.

Pretty scary stuff!

## How it Works

### Rules

The story generator uses a simple rule-based grammar to describe a story. Stories are composed of atomic rules that are composed together using other rules, then built into a story by choosing one rule to rule them all.

Each rule is a single word (also called a token) at the beginning of a new line. The next line (or lines, as we'll see) are the various forms of the rule. For example, if you're greeting somebody, you might say `Hi!`, or `Hello!`, or even `How are you?`. In our grammar, we might represent that as follows:

    Greeting
      "Hi!"
      "Hello!"
      "How are you?"

If we want to indicate that a greeting can be one of three static responses, we wrap that text inside of double-quotes. Each line is a new form that the rule could take. If we generate a greeting, our rule gives us one of three possible responses.

Things get interesting when we consider that rules can also be made up from other rules. For example, consider this:

    Story
      Beginning End

    Beginning
      "The cat "
      "The dog "

    End
      "was nice."
      "was happy."

If we use `Story` as the "starting" rule, like `Greeting` in the previous example, we see that a `Story` is made up from a `Beginning` and an `End`. There are two possible beginnings, and two possible endings. If this was our story generator, we would see stories like this:

    The dog was happy.
    The cat was happy.
    The cat was nice.

I'm sure you'll agree, those are lovely stories.

### The Generate command

To use this in our story generator, we just need one more piece. We've talked about using `Story` as our main rule, so we just need to make sure the generator knows what we're thinking. If we start a new line with the word (or token) `Generate`, we'll be able to inform the program how to write stories using our friendly grammar.

    Generate Story

The complete example is in `stories/animals.txt`, and you can generate stories using the following command:

    python parser.py stories/animals.txt

### Variables, to make things interesting

If we just use rules, our stories might get boring after a while. Our animals example is illustrative, but there are a maximum of four different stories. One way to make things more interesting is to introduce variables.

By using the `Use` command, along with a variable type, and a text file with a collection of possible replacements on each line, we can define a variable for use in our grammar.

What does this mean? Let's consider the file `text/animals.txt`, included here in full:

    dog
    cat
    otter
    lion
    mouse
    aardvark
    elephant
    bird

As you can see, this is a comprehensive list of every animal. (Okay, I might have missed one or two!) Let's modify our animal story generator above to `Use` the `Animal` list found in `text/animals.txt`.

    Use Animal text/animals.txt

    Story
      Beginning End

    Beginning
      "The " Animal.MyAnimal " "
      "The " Animal.MyAnimal " "

    End
      "was nice."
      "was happy."

    Generate Story

There are two main differences from our earlier example.

First is the line beginning with `Use`, which says that we'd like to define a new variable of type `Animal`, which must take on one of the values found on one of the lines in `text/animals.txt`. This means that when we get an `Animal` in one of our rules, we'd like to insert one of the possibilities found in `text/animals.txt`.

Second, we've wrapped up our text in double-quotes again inside the `Beginning` rule, but we've inserted `Animal.MyAnimal` (we'll explain this in the next paragraph!) and glued three pieces together. The first piece is the text `"The "` (note the space). The third piece is the text `" "` (just a single space!). The middle piece is a reference to the Animal variable, indicated by the fact that it's not inside double-quotes, and the presence of the period. The left side of the period indicates the variable we want to substitute (`Animal`), and the right side is an optional variable name, if we want to use this same variable again later in our story. (We could have written `Animal.` instead of `Animal.MyAnimal`)

Let's see what a few runs of this program looks like:

    python parser.py stories/animals-variable.txt
    Starting rule: ['Story']
    Setting MyAnimal (Animal) to value dog
    The dog was happy.

and..

    python parser.py stories/animals-variable.txt
    Starting rule: ['Story']
    Setting MyAnimal (Animal) to value aardvark
    The aardvark was nice.

By default, the parser will let you know when a value has been assigned to a variable, as in our use of `MyAnimal` with the `Animal` variable. If we'd used `Animal.MyAnimal` in the `End` rule, it would have been the same value found earlier in the story. For example, if we wrote this:

    End
      "was a nice " Animal.MyAnimal "."
      "was a happy " Animal.MyAnimal "."

We might see output like this:

    The dog was a happy dog.
    The aardvark was a nice aardvark.
