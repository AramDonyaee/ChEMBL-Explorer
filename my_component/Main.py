import os
import base64
import mols2grid
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from rdkit import Chem
from rdkit.Chem.Descriptors import ExactMolWt

from chembl_webresource_client.new_client import new_client
from chembl_webresource_client.http_errors import BaseHttpException

# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
# (This is, of course, optional - there are innumerable ways to manage your
# release process.)
_RELEASE = False

# Declare a Streamlit component. `declare_component` returns a function
# that is used to create instances of the component. We're naming this
# function "_component_func", with an underscore prefix, because we don't want
# to expose it directly to users. Instead, we will create a custom wrapper
# function, below, that will serve as our component's public API.

# It's worth noting that this call to `declare_component` is the
# *only thing* you need to do to create the binding between Streamlit and
# your component frontend. Everything else we do in this file is simply a
# best practice.

if not _RELEASE:
    _component_func = components.declare_component(
        # We give the component a simple, descriptive name ("my_component"
        # does not fit this bill, so please choose something better for your
        # own component :)
        "my_component",
        # Pass `url` here to tell Streamlit that the component will be served
        # by the local dev server that you run via `npm run start`.
        # (This is useful while your component is in development.)
        url="http://localhost:3001",
    )
else:
    # When we're distributing a production version of the component, we'll
    # replace the `url` param with `path`, and point it to to the component's
    # build directory:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("my_component", path=build_dir)


def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="bioactivitydata.csv">Download csv file</a>'
    return href

# Create a wrapper function for the component. This is an optional
# best practice - we could simply expose the component function returned by
# `declare_component` and call it done. The wrapper allows us to customize
# our component's API: we can pre-process its input args, post-process its
# output value, and add a docstring for users.
def my_component(fileData, key=None):
    """Create a new instance of "my_component".

    Parameters
    ----------
    name: str
        The name of the thing we're saying hello to. The component will display
        the text "Hello, {name}!"
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.

    Returns
    -------
    int
        The number of times the component's "Click Me" button has been clicked.
        (This is the value passed to `Streamlit.setComponentValue` on the
        frontend.)

    """
    # Call through to our private component function. Arguments we pass here
    # will be sent to the frontend, where they'll be available in an "args"
    # dictionary.
    #
    # "default" is a special argument that specifies the initial return
    # value of the component before the user has interacted with it.
    component_value = _component_func()

    # We could modify the value returned from the component if we wanted.
    # There's no need to do this in our simple example - but it's an option.
    return component_value


# Add some test code to play with the component while it's in development.
# During development, we can run this just as we would any other Streamlit
# app: `$ streamlit run my_component/__init__.py`
if not _RELEASE:

    st.markdown(""" <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style> """, unsafe_allow_html=True)

    st.title("Chembl Explorer")


    st.markdown("<h2><strong>Step 1:</strong> Search for a disease or a target</h2>", unsafe_allow_html=True)
    user_input = st.text_input("Type the name of the disease or target here")

    if user_input: 
        

        try:
            target = new_client.target
            target_query = target.search(user_input)
            targets = pd.DataFrame.from_dict(target_query)

            if len(targets) > 0:
                st.write(targets)

                st.markdown("<h2><strong>Step 2:</strong> Select a specific target to get Bio Activity</h2>", unsafe_allow_html=True)
                selected_indice = st.selectbox('Select a target:', targets.target_chembl_id, index=0)
                selected_indice_final = targets.loc[targets['target_chembl_id'] == selected_indice]
                st.subheader("Your selected target")
                selected_indice_final

                if selected_indice:
                    activity = new_client.activity
                    response = activity.filter(target_chembl_id=selected_indice).filter(standard_type="IC50")
                    response = pd.DataFrame.from_dict(response)

                    if len(response) > 0:
                        st.subheader('Bio Activty summary for the selected target')
                        st.write(response.head(10))

                        st.markdown("<h2><strong>Step 3:</strong> Download customized Bio Activity dataset</h2>", unsafe_allow_html=True)
                        selected_columns = st.multiselect('Select columns (if you do not select any, all of the columns will be included in dataset)', response.columns)
                        selection = selected_columns

                        if not selection:
                            response = response
                        else:
                            response = response[selection]

                        st.markdown(get_table_download_link(response), unsafe_allow_html=True)

                    else:
                        st.write('There was no bioactivity data available for the selected target')

        except BaseHttpException:
            st.error("Please try another query")

 

    # conponent initializatio example for future use cases
    # component_stance = my_component()

