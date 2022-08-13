from hydralit import HydraApp
import streamlit as st

app = HydraApp(title='Sample Hydralit App',favicon="🐙")
  
#add all your application classes here
app.add_app("Small App", icon="🏠", app=MySmallApp())
app.add_app("Sample App",icon="🔊", app=MySampleApp())

    #run the whole lot
app.run()
