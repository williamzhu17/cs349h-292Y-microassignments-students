### Part A: Hyperdimensional Computing [8 pts total, 2 pts / question]

**Task 1:** In `hdc.py`, implement the hypervector generation, binding, bundling, Hamming distance, and permutation operations in the scaffold code. Also, implement the `add` and `get` functions in the item memory `HDItemMem` class; these functions will be used to manage the atomic hypervectors. Based on them, implement an HD encoding procedure that encodes strings in `make_word` function. You should also implement the `make_letter_hvs` function. It should produce a codebook for the letters, which serves as the first argument for the `make_word` function. Refer to the main scripts for how these two functions are invoked in sequence.

For example "fox" would be translated to sequence ["f","o", "x"]. For simplicity, use a hypervector size of 10,000 to answer these questions unless otherwise stated.

**Q1.** Construct a HDC-based string encoding for the word "fox". How did you encode the "fox" string? How similar is the hypervector for "fox" to the hypervector for "box" in your encoding? How similar is the hypervector for "xfo"? How similar is the hypervector for "car"? Please remark on the relative similarities, not the absolute distances.

I encoded the "fox" string by generating a unique hypervector for each letter of the english alphabet. Using these hypervectors, I was able to then construct words, like "fox" by permuting each letter's hypervector to the specific index of the word and then bundling them together. 

By running the program, I see that the distance between "fox" and "box" is significantly lower than the distance between "fox" and "xfo" and "fox" and "car". Quantitatively, the distance between "fox" and "box" was 0.2407, the distance between "fox" and "xfo" was 0.5023, and the distance between "fox" and "car" was 0.5107. 

**Q2.** Change your encoding so the order of the letters doesn't matter (apply the changes for this question only). What changes did you make? Please remark on the relative similarities, not the absolute distances.

After changing the encoding so the order of the letters do not matter, I see that "fox" and "xfo" are now the closest. However, "fox" and "box" are still more similar than "fox" and "car". 

Quantitatively, I saw the distance between "fox" and "box" was 0.2544, the distance between "fox and xfo" was 0, and the distance between "fox" and "car" was 0.5003. 

To make this change, I just removed the functionality of permuting the letter vectors before bundling them. This removed any sense of position in the word. 

-------

**Task 2:**: Implement the bit flip error helper function (`apply_bit_flips`). Then apply bit flip errors to hypervectors before the distance calculations, where the bit flip probability is 0.10. Specifically, before computing the distance between two hypervectors hv1 and hv2, you may apply the bit flip error to one of them, say hv1. Use the `monte_carlo`, `study_distributions`, and `plot_hist_distributions` helper functions to study the distribution of distances between `fox` and `box`, compared to the distance between `fox` and `car` with and without hardware error.

**Q3.** Try modifying the hardware error rate (`perr`) with fixed hypervector size `10000`. How high can you make the hardware error until the two distributions begin to become visibly indistinguishable? What does it mean conceptually when the two distance distributions have a lot of overlap?

Starting at around a perr of 0.45, we start to see the distributions overlap. At around a perr of 0.5, it is very hard to visible distibuguish the two distributions. 

When the two distance distributions have a lot of overlap, this means that the hypervectors are starting to have a lot more noise from the bitflips and lose the similarity/difference signals that the bundling of the permuted letter hypervectors had. 

**Q4.** Try modifying the hypervector size (`SIZE`) with fixed hardware error rate `0.10`. How small can you make the word hypervectors before the two distributions begin to become visibly indistinguishable?

There starts to be overlap when SIZE is around 100. At 10, the distributions start to become visible indistinguishable. 

-----

**Task 3:**: Next, fill out the stubs in the item memory class -- there are stubs for threshold-based (`matches`) and winner-take-all (`wta`) queries, and for computing the Hamming distances between item memory rows and the query hypervector. The item memory class will be used in later exercises to build a database data structure and an ML model.

### Part B: Item Memories [`hdc-db.py`, 10 points total, 2 pts / question]

Next, we will use this item memory to implement a database data structure; we will be performing queries against an HDC-based database populated with the digimon dataset (`digimon.csv`). The HDDatabase class implements the hyperdimensional computing-based version of this data structure, and contains stubs of convenience functions for encoding / decoding strings and database rows, as well as stubs for populating and querying the database. We will implement this class and then invoke `build_database` to build a database using the HDDatabase class. For simplicity, use a hypervector size of 10,000 to answer these questions unless otherwise stated.

_Tip_: For this exercise, map every distinct string to an atomic random hypervector. This will keep retrieval tasks relatively simple. For decoding operations, you will likely need to use the self-inverse property of binding and perform additional lookups to recover information.

---------

__Task 0__: The database data structure contains multiple rows, where each row is uniquely identified with a primary key and contains a collection of fields that are assigned to values. In the HD implmentation, the database rows are maintained in item memories, and row data is encoded as a hypervector. Decide how you want to map the database information to item memories. Implement the database row addition `add_row` function, which should invoke the `encode_row` helper function and update the appropriate item memories.

---------

__Task 1__: Implement the string and row encoding functions (`encode_string`, `encode_row`). These encoding functions accept a string and a database row (field-value map) respectively, and translate these inputs into hypervectors by applying HD operators to atomic basis vectors. Then, implement the string and row decoding functions (`decode_string`, `decode_row`) which take the hypervector representations of a string or database row respectively and reconstructs the original data. The decoding routines will likely need to perform multiple codebook / item memory lookups and use HD operator properties (e.g., unbinding) to recover the input data. Execute `digimon_test_encoding` function to test your string and row encoding routines and verify that you're able to recover information from the hypervector embedding with acceptable reliability.

**Q1.** Describe how you encoded database rows as hypervectors. Write out the HD expression you used to encode each piece of information, and describe any atomic hypervectors you introduced.

For each field name and value pair in the row, I first encoded the field name and value into a hypervector. If the field name or the value was not already in the codebook, we would introduce a atomic hypervector here. Afterwards, I then bound the two together to create a tuple. These created each field and value pair. 

After iterating through all field name and value pairs, I then bundled them together to create the database row. 

**Q2.** Describe how you decoded the strings / database rows from hypervectors. Describe any HD operations you used to isolate the desired piece of information, and describe what item memory lookups you performed to recover information. If you're taking advantage of any HD operator properties to isolate information, describe how they do so.

To decode a string, I would take the hypervector form of the string. Then, I would loop through all the possible strings in the codebook and find the one that is closest hamming distance. This would then be the decoded string. 

To decode a row, I iterated through all of our field names, as it would be the same amongst each row. For each field name, I would first bind the hypervector version of the field name to the row hypervector. This would undo the prior bind operation and isolate the value of that particular field. After that, I would then just do a winner takes all decode of the resulting hypervector. In theory, after unbinding the one tuple in my row, the string in the codebook that is closest in distance to this resulting hypervector should be my value of the field. I repeated this process, iterating through each of the field names and filling out the field values. 

--------

__Task 2__: Next, we'll implement routines for querying the data structure. Implement the `get_value` and `get_matches` stubs -- the `get_value` query retrieves the value assigned to a user-provided field within a record. The `get_matches` stub retrieves the rows that contain a subset of field-value pairs. Implement both these querying routines and then execute `digimon_basic_queries` and `digimon_value_queries` to test your implementations.

**Q3.** How did you implement the `get_value` query? Describe any HD operators and lookups you performed to implement this query.

I implemented the get_value query by first obtaining the hypervector associated with the key. After doing so, I would decode the row. More details on how decoding the row can be found in the prior question response. 

**Q4.** How did you implement the `get_matches` query? Describe any HD operators and lookups you performed to implement this query. Try using lower threshold values. How high of a distance threshold can you set before you start seeing false positives in the returned results?

I implemented the get_matches by first converting the field_value_dict into a hypervector. To do this, we encoded each of the field value pairs in the query into a tuple by encoding each field name and value into a tuple and then binding them together. Once we have a hypervector for each field value pair, we would then bundle them together to create the query vector. We then use the query vector and see the hamming distance of each row in the db. If they are lower than the threshold, we have a match. 

At a threshold of around 0.45, I started seeing false positives in the returned results. 

-----

__Task 3__: Implement the `get_analogy` query, which given two records and a value in one of the records, identifies the value that shares the same field in the other record as the input value. For example, if you perform an `analogy` query on the `US` and `Mexico` records, and ask for the value in the `Mexico` record that relates to the `Dollar` value in the `US` record, this query would return `Peso`. This query completes the analogy  _Dollar is to USA as <result> is to Mexico_. Execute `analogy_query` to test your implementation.

_Tip_: If you want more information on this type of query, you can look up "What We Mean When We Say 'What's the Dollar of Mexico?'"

**Q5.** How did you implement the `get_analogy` query? Describe how this is implemented using HD operators and item memory lookups. Why does your implementation work? You may want to walk through and HD operator properties you leveraged to complete this query.

To implement get_analogy, I first obtained the hypervectors of both the row entries. Then, with the target row, I bound the hypervector version of the target value to the target hypervector row. This allowed me to isolate the field name of that value. Then, I used the codebook and picked the string hypervecotr that was closest to this resulting vector to figure out what the field name was. 

Once I had the field name, I did the opposite. I bound the hypervector version of the field name to the other hypervector row, isolating the value information of that field. Then, I used the codebook and picked the string hypervector that was closest to this resulting vector to figure out what the value was. The distance that was computed between the closest string hypervector and the resulting hypervector was saved and returned as well. 

### Part C: Implementing an HDC Classifier [10 pts total, 2 pts/question, hdc-ml.py]

Next, we will use an item memory to implement an MNIST image classifier. A naive implementation of this classifier should easily be able to get ~75% accuracy. In literature, HDC-based MNIST classifiers have been shown to achieve ~98% classification accuracy with model size of only a few bytes while being error resilient. In this exercise, you will implement the necessary encoding/decoding routines, and you will implement both the training and inference algorithms for the classifier.

__Tips__: Try a simple pixel/image encoding first. For decoding operations, you will likely need to use the self-inverse property of binding to recover information.

-------------

**Task 1**: Fill in the `encode_pixel`, `decode_pixel`, `encode_image`, and `decode_image` stubs in the MNIST classifier. These functions should translate pixels/images to/from their hypervector representation. Then use the `test_encoding` function to evaluate the quality of your encoding. This function will save the original image to `sample0.png`, and the encoded then decoded image to `sample0_rec.png`.

**Q1.** How did you encode pixels as a hypervector? Write out the HD expressions, and describe what atomic/basis hypervectors you used for the encodings. 

To encode a pixel, I first encoded a coordinate. To encode a coordinate, I built a codebook for coordinate values so each coordinate number would get an atomic hypervector. Then to build the coordinate, I would first permute the j hypervector by 1 and then bind it with the i hypervector. This gave me a hypervector for the coordinates. 

Then for the pixels, I created a new codebook for the value of the pixel. This way, the value numbers would get its own atomic hypervector. I would then take the value hypervector of the pixel and bind it with the coordinate hypervector. 

**Q2.** How did you encode images as a hypervector? Write out the HD expressions, and describe any atomic/basis hypervectors in the expression. 

I encoded the image as a hypervector by first computing the hypervector encoding of each pixel. Then, based on each of the pixels location, I would permute the pixel's hypervector by i*MAX + j. This way, each pixel would have a unique location. Then, I would just bundle all the permuted pixel hypervectors together. 

-----------------------

**Task 2**: Fill in the `train` and the `classify` stubs in the MNIST classifier. Test your classifier out by invoking the `test_classifier` function. What classification accuracy did you attain? You should be able to achieve ~75% with the standard techniques learned in class. We will give full credit for accuracy about or above 75%.

**Q3.** What happens to the classification accuracy when you reduce the hypervector size; how small of a size can you select before you see > 5% loss in accuracy? 

**Q4.** What happens to the classification accuracy when you introduce bit flips into the item memory's distance calculation? Note that you shold only apply bit flips during inference. How much error can you introduce before you see a > 5% loss in accuracy?

------------------------

**Task 3**: You can also implement a simple generative model using hyperdimensional computing. In this following exercise, we will use HDC to generate images of handwritten digits from the classifier label. Naive HD generative models are very similar to HD classifiers, and are constructed in two simple steps:

- _Constructing a Generative Model._ For each classifier label, group training data by label, and translate each datum to a hypervector. Next, generate a probability vector for each label. The probability value at position i of the probability vector is the probability that the hypervector bit in position i is a "1" bit value. The probability vector can easily be computed by summing up the M hypervectors that share the same label, and then normalizing by 1/M.

- _Generating Random Images._ To generate a random image for some label, you sample a binary hypervector from the probability hypervector for that label. You then translate the hypervector to an image using the hypervector decoding routine (`decode_image`). You can sample and bundle multiple hypervectors to average the result.

You can find a sample of generated image `sample_generated.png` for number `7` in the folder.

**Q5.** Use `test_generative_model` function to test your generative model. Include a few pictures outputted by your generative model in your submission.
