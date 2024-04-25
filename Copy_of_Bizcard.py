{
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/TheQueenUma/Phonepe-Pulse-Data-Visualization/blob/main/Copy_of_Bizcard.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "4KMuM93baa22"
      },
      "outputs": [],
      "source": [
        "!pip install easyocr"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "DtL0jBpUamvb"
      },
      "outputs": [],
      "source": [
        "!pip install streamlit"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "LvnadKDRayjh"
      },
      "outputs": [],
      "source": [
        "!pip install streamlit_option_menu"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "EkC10HgtbMai"
      },
      "outputs": [],
      "source": [
        "import streamlit as st\n",
        "from streamlit_option_menu import option_menu\n",
        "import easyocr\n",
        "from PIL import Image\n",
        "import pandas as pd\n",
        "import numpy as np\n",
        "import re\n",
        "import io\n",
        "import sqlite3\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "4j-VmKQAcEIb"
      },
      "outputs": [],
      "source": [
        "def image_to_text(path):\n",
        "\n",
        "  input_img=Image.open(path)\n",
        "\n",
        "  #converting image to array format\n",
        "\n",
        "  image_arr=np.array(input_img)\n",
        "\n",
        "  reader=easyocr.Reader(['en'])\n",
        "  text=reader.readtext(image_arr,detail=0)\n",
        "\n",
        "  return text, input_img\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "J-Z8_o1TdX-B"
      },
      "outputs": [],
      "source": [
        "text_img,input_img=  image_to_text(\"/content/1.png\")"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "jGjc1qcd_ilR"
      },
      "outputs": [],
      "source": [
        "text_img,input_img=  image_to_text(\"/content/2.png\")"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "BA6BQbQy_wcB"
      },
      "outputs": [],
      "source": [
        "text_img,input_img=  image_to_text(\"/content/3.png\")"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "pIfBMdSB_31D"
      },
      "outputs": [],
      "source": [
        "text_img,input_img=  image_to_text(\"/content/4.png\")"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "uh850IVl_6e-"
      },
      "outputs": [],
      "source": [
        "text_img,input_img=  image_to_text(\"/content/5.png\")"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "4FHYcuqKnmIF"
      },
      "outputs": [],
      "source": [
        "def extracted_text(texts):\n",
        "\n",
        "  extrd_dict={\"NAME\":[], \"DESIGNATION\":[], \"COMPANY_NAME\":[], \"CONTACT\":[],\"EMAIL\":[], \"WEBSITE\":[],\n",
        "              \"ADDRESS\" :[], \"PINCODE\":[]}\n",
        "\n",
        "  extrd_dict[\"NAME\"].append(texts[0])\n",
        "  extrd_dict[\"DESIGNATION\"].append(texts[1])\n",
        "\n",
        "\n",
        "  for i in range(2,len(texts)):\n",
        "\n",
        "    if texts[i].startswith(\"+\") or (texts[i].replace(\"-\",\"\").isdigit() and '-' in texts[i]):\n",
        "       extrd_dict[\"CONTACT\"].append(texts[i])\n",
        "\n",
        "    elif \"@\" in texts[i] and \".com\" in texts[i]:\n",
        "       extrd_dict[\"EMAIL\"].append(texts[i])\n",
        "\n",
        "    elif \"WWW\" in texts[i] or \"www\" in texts[i] or \"wWW\" in texts[i] or \"wwW\" in texts[i]:\n",
        "      small=texts[i].lower()\n",
        "      extrd_dict[\"WEBSITE\"].append(small)\n",
        "\n",
        "    elif \"Taamil Nadu\" in texts[i] or \"TamilNadu\" in texts[i] or texts[i].isdigit():\n",
        "      extrd_dict[\"PINCODE\"].append(texts[i])\n",
        "\n",
        "    elif re.match(r'^[A-Za-z]', texts[i]):\n",
        "      extrd_dict[\"COMPANY_NAME\"].append(texts[i])\n",
        "\n",
        "    else:\n",
        "      remove_colon=re.sub(r'[,;]','',texts[i])\n",
        "      extrd_dict[\"ADDRESS\"].append(remove_colon)\n",
        "\n",
        "  for key,value in  extrd_dict.items():\n",
        "    if len(value)>0:\n",
        "      concatenate=\" \".join(value)\n",
        "      extrd_dict[key]=[concatenate]\n",
        "\n",
        "    else:\n",
        "        value=\"NA\"\n",
        "        extrd_dict[key]=[value]\n",
        "\n",
        "\n",
        "\n",
        "  return extrd_dict"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "B4B4faL4yqMw"
      },
      "outputs": [],
      "source": [
        "text_data = extracted_text(text_img)\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "jD8Zg-AWyufl"
      },
      "outputs": [],
      "source": [
        "df = pd.DataFrame(text_data)\n",
        "df"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "gF_5Pe1UyC7X"
      },
      "outputs": [],
      "source": [
        "text_img"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "IXS1zT3ww17v"
      },
      "outputs": [],
      "source": [
        "# converting Image to Bytes\n",
        "\n",
        "Image_bytes = io.BytesIO()\n",
        "input_img.save(Image_bytes, format= \"PNG\")\n",
        "\n",
        "image_data = Image_bytes.getvalue()\n",
        "\n",
        "#creating Dictionry\n",
        "data = {\"IMAGE\":[image_data]}\n",
        "\n",
        "\n",
        "df_1 = pd.DataFrame(data)\n",
        "\n",
        "concat_df= pd.concat([df,df_1],axis=1 )\n",
        "concat_df\n"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "from google.colab import drive\n",
        "drive.mount('/content/drive')"
      ],
      "metadata": {
        "id": "gPoFhxv6J-5w"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "FA85VTtm7_98"
      },
      "outputs": [],
      "source": [
        "mydb = sqlite3.connect(\"bizcardx.db\")\n",
        "cursor = mydb.cursor()\n",
        "\n",
        "#Table creation\n",
        "\n",
        "create_table_query = ''' CREATE TABLE IF NOT EXISTS bizcard_details(name varchar(255),\n",
        "                                                                   designation varchar(255),\n",
        "                                                                   company_name varchar(255),\n",
        "                                                                   contact varchar(255),\n",
        "                                                                    email varchar(255),\n",
        "                                                                    website text,\n",
        "                                                                    address text,\n",
        "                                                                    pincode varchat(255),\n",
        "                                                                    image text)'''\n",
        "\n",
        "cursor.execute(create_table_query)\n",
        "mydb.commit()\n",
        "\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "me68TiUz8Og-"
      },
      "outputs": [],
      "source": [
        "#Insert query\n",
        "\n",
        "insert_query = ''' INSERT INTO bizcard_details(name,designation,company_name,contact,email,website,address,pincode,image)\n",
        "                                               values(?,?,?,?,?,?,?,?,?)'''\n",
        "datas = concat_df.values.tolist()\n",
        "cursor.executemany(insert_query, datas)\n",
        "mydb.commit()\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "tRDpaHTZ-v5h"
      },
      "outputs": [],
      "source": [
        "#select Query\n",
        "\n",
        "select_query = \" SELECT * FROM bizcard_details \"\n",
        "cursor.execute(select_query)\n",
        "table = cursor.fetchall()\n",
        "mydb.commit()\n",
        "\n",
        "table_df = pd.DataFrame(table, columns=(\"NAME\",\"DESIGNATION\", \"COMPANY NAME\",\"CONTACT\",\"EMAIL\",\"WEBSITE\",\"ADDRESS\",\"PINCODE\",\"IMAGE\"))\n",
        "table_df\n",
        "\n",
        "\n",
        "\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "SGgLbK0_9Kz9"
      },
      "outputs": [],
      "source": [
        "concat_df"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "G7N2dbVcy9JK"
      },
      "outputs": [],
      "source": [
        "\n",
        "\n",
        "import streamlit as st\n",
        "from streamlit_option_menu import option_menu\n",
        "import easyocr\n",
        "from PIL import Image\n",
        "import pandas as pd\n",
        "import numpy as np\n",
        "import re\n",
        "import io\n",
        "import sqlite3\n",
        "\n",
        "def image_to_text(path):\n",
        "\n",
        "  input_img=Image.open(path)\n",
        "\n",
        "  #converting image to array format\n",
        "\n",
        "  image_arr=np.array(input_img)\n",
        "\n",
        "  reader=easyocr.Reader(['en'])\n",
        "  text=reader.readtext(image_arr,detail=0)\n",
        "\n",
        "  return text, input_img\n",
        "\n",
        "def extracted_text(texts):\n",
        "\n",
        "  extrd_dict={\"NAME\":[], \"DESIGNATION\":[], \"COMPANY_NAME\":[], \"CONTACT\":[],\"EMAIL\":[], \"WEBSITE\":[],\n",
        "              \"ADDRESS\" :[], \"PINCODE\":[]}\n",
        "\n",
        "  extrd_dict[\"NAME\"].append(texts[0])\n",
        "  extrd_dict[\"DESIGNATION\"].append(texts[1])\n",
        "\n",
        "\n",
        "  for i in range(2,len(texts)):\n",
        "\n",
        "    if texts[i].startswith(\"+\") or (texts[i].replace(\"-\",\"\").isdigit() and '-' in texts[i]):\n",
        "       extrd_dict[\"CONTACT\"].append(texts[i])\n",
        "\n",
        "    elif \"@\" in texts[i] and \".com\" in texts[i]:\n",
        "       extrd_dict[\"EMAIL\"].append(texts[i])\n",
        "\n",
        "    elif \"WWW\" in texts[i] or \"www\" in texts[i] or \"wWW\" in texts[i] or \"wwW\" in texts[i]:\n",
        "      small=texts[i].lower()\n",
        "      extrd_dict[\"WEBSITE\"].append(small)\n",
        "\n",
        "    elif \"Taamil Nadu\" in texts[i] or \"TamilNadu\" in texts[i] or texts[i].isdigit():\n",
        "      extrd_dict[\"PINCODE\"].append(texts[i])\n",
        "\n",
        "    elif re.match(r'^[A-Za-z]', texts[i]):\n",
        "      extrd_dict[\"COMPANY_NAME\"].append(texts[i])\n",
        "\n",
        "    else:\n",
        "      remove_colon=re.sub(r'[,;]','',texts[i])\n",
        "      extrd_dict[\"ADDRESS\"].append(remove_colon)\n",
        "\n",
        "  for key,value in  extrd_dict.items():\n",
        "    if len(value)>0:\n",
        "      concatenate=\" \".join(value)\n",
        "      extrd_dict[key]=[concatenate]\n",
        "\n",
        "    else:\n",
        "        value=\"NA\"\n",
        "        extrd_dict[key]=[value]\n",
        "\n",
        "\n",
        "\n",
        "  return extrd_dict\n",
        "\n",
        "\n",
        "\n",
        "\n",
        "\n",
        "\n",
        "\n",
        "\n",
        "\n",
        "\n",
        "\n",
        "#streamlit part\n",
        "st.set_page_config(layout= \"wide\")\n",
        "st.title(\"EXTRACTION BUSINESS CARD DATA WITH 'OCR' \")\n",
        "\n",
        "with st.sidebar:\n",
        "  select=option_menu(\"Main Menu\", [\"Home\",\"Upload & Modifying\",\"Delete\"])\n",
        "\n",
        "if select == \"Home\":\n",
        "  pass\n",
        "\n",
        "elif select == \"Upload & Modifying\":\n",
        "  img = st.file_uploader(\"Upload the Imaage\", type=[\"png\",\"jpg\",\"jpeg\"])\n",
        "  if img is not None:\n",
        "    st.image(img, width=300)\n",
        "\n",
        "    text_image, input_img = image_to_text(img)\n",
        "\n",
        "    text_dict = extracted_text(text_image)\n",
        "\n",
        "    if text_dict:\n",
        "      st.success(\"TEXT IS EXTRACTED SUCCESSFULLY\")\n",
        "\n",
        "    df = pd.DataFrame(text_dict)\n",
        "\n",
        "    # converting Image to Bytes\n",
        "\n",
        "    Image_bytes = io.BytesIO()\n",
        "    input_img.save(Image_bytes, format= \"PNG\")\n",
        "\n",
        "    image_data = Image_bytes.getvalue()\n",
        "\n",
        "    #creating Dictionry\n",
        "    data = {\"IMAGE\":[image_data]}\n",
        "\n",
        "\n",
        "    df_1 = pd.DataFrame(data)\n",
        "\n",
        "    concat_df= pd.concat([df,df_1],axis=1 )\n",
        "\n",
        "    st.dataframe(concat_df)\n",
        "\n",
        "    button_1 = st.button(\"save\")\n",
        "\n",
        "    if button_1:\n",
        "\n",
        "      mydb = sqlite3.connect(\"bizcardx.db\")\n",
        "      cursor = mydb.cursor()\n",
        "\n",
        "      #Table creation\n",
        "\n",
        "      create_table_query = ''' CREATE TABLE IF NOT EXISTS bizcard_details(name varchar(255),\n",
        "                                                                        designation varchar(255),\n",
        "                                                                        company_name varchar(255),\n",
        "                                                                        contact varchar(255),\n",
        "                                                                          email varchar(255),\n",
        "                                                                          website text,\n",
        "                                                                          address text,\n",
        "                                                                          pincode varchat(255),\n",
        "                                                                          image text)'''\n",
        "\n",
        "      cursor.execute(create_table_query)\n",
        "      mydb.commit()\n",
        "\n",
        "      #Insert query\n",
        "\n",
        "      #Insert query\n",
        "\n",
        "      insert_query = ''' INSERT INTO bizcard_details(name,designation,company_name,contact,email,website,address,pincode,image)\n",
        "                                                    values(?,?,?,?,?,?,?,?,?)'''\n",
        "      datas = concat_df.values.tolist()\n",
        "      cursor.executemany(insert_query, datas)\n",
        "      mydb.commit()\n",
        "\n",
        "      st.success(\"SAVED SUCCESSFULLY\")\n",
        "\n",
        "  method = st.radio(\"select the method\",[\"None\",\"preview\",\"Modify\"])\n",
        "  if method== \"None\":\n",
        "\n",
        "    st.write(\"\")\n",
        "\n",
        "  if method ==\"preview\":\n",
        "        #select Query\n",
        "\n",
        "    mydb = sqlite3.connect(\"bizcardx.db\")\n",
        "    cursor = mydb.cursor()\n",
        "\n",
        "    select_query = \" SELECT * FROM bizcard_details \"\n",
        "    cursor.execute(select_query)\n",
        "    table = cursor.fetchall()\n",
        "    mydb.commit()\n",
        "\n",
        "    table_df = pd.DataFrame(table, columns=(\"NAME\",\"DESIGNATION\", \"COMPANY NAME\",\"CONTACT\",\"EMAIL\",\"WEBSITE\",\"ADDRESS\",\"PINCODE\",\"IMAGE\"))\n",
        "    st.dataframe(table_df)\n",
        "\n",
        "  elif method == \"Modify\":\n",
        "\n",
        "    mydb = sqlite3.connect(\"bizcardx.db\")\n",
        "    cursor = mydb.cursor()\n",
        "\n",
        "    select_query = \" SELECT * FROM bizcard_details \"\n",
        "    cursor.execute(select_query)\n",
        "    table = cursor.fetchall()\n",
        "    mydb.commit()\n",
        "\n",
        "    table_df = pd.DataFrame(table, columns=(\"NAME\",\"DESIGNATION\", \"COMPANY NAME\",\"CONTACT\",\"EMAIL\",\"WEBSITE\",\"ADDRESS\",\"PINCODE\",\"IMAGE\"))\n",
        "\n",
        "    col1,col2 = st.columns(2)\n",
        "    with col1:\n",
        "\n",
        "      selected_name = st.selectbox(\"Select the name\",table_df[\"NAME\"])\n",
        "\n",
        "    df_3 = table_df[table_df[\"NAME\"]== selected_name]\n",
        "\n",
        "    st.dataframe(df_3)\n",
        "\n",
        "    df_4 = df_3.copy\n",
        "\n",
        "    st.dataframe(df_3)\n",
        "\n",
        "    col1,col2= st.columns(2)\n",
        "    with col1:\n",
        "      mo_name=st.text_input(\"Name\",df_3[\"NAME\"].unique()[0])\n",
        "\n",
        "\n",
        "\n",
        "\n",
        "\n",
        "\n",
        "\n",
        "\n",
        "elif select == \"Delete\":\n",
        "\n",
        "  mydb = sqlite3.connect(\"bizcardx.db\")\n",
        "  cursor = mydb.cursor()\n",
        "\n",
        "  col1,col2 = st.columns(2)\n",
        "  with col1:\n",
        "\n",
        "    select_query = \"SELECT NAME FROM bizcard_details\"\n",
        "\n",
        "    cursor.execute(select_query)\n",
        "    table1= cursor.fetchall()\n",
        "    mydb.commit()\n",
        "\n",
        "    names =[]\n",
        "\n",
        "    for i in table1:\n",
        "      names.append(i[0])\n",
        "\n",
        "    name_select = st.selectbox(\"Select the name\",names)\n",
        "\n",
        "  if name_select:\n",
        "    col1,col2 = st.columns(2)\n",
        "    with col1:\n",
        "      st.write(\"Select Name : {name_select}\")\n",
        "\n",
        "      remove = st.button(\"Delete\", use_container_width=True)\n",
        "\n",
        "      if remove:\n",
        "        cursor.execute(f\"DELETE from bizcard_details WHERE NAME = '{name_select}' \")\n",
        "\n",
        "        mydb.commit()\n",
        "\n",
        "        st.warning(\"DELETED\")\n",
        "\n",
        "\n",
        "\n",
        "\n",
        "\n",
        "\n",
        "\n",
        "\n",
        "\n",
        "\n",
        "\n",
        "\n",
        "\n",
        "\n",
        "\n",
        "\n",
        "\n",
        "\n",
        "\n",
        "\n",
        "\n",
        "\n",
        "\n",
        "\n",
        "\n",
        "\n",
        "\n",
        "\n",
        "\n",
        "\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "jnT_eOv4pzT1"
      },
      "outputs": [],
      "source": [
        "!wget -q -O - ipv4.icanhazip.com"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {
          "background_save": true
        },
        "id": "DHplYh5eqqE2"
      },
      "outputs": [],
      "source": [
        "!streamlit run my_app.py & npx localtunnel --port 8501"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "iL12oWlkrCSp"
      },
      "outputs": [],
      "source": []
    }
  ],
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyPM9B6H7t4lV1LcPMhSkCrH",
      "include_colab_link": true
    },
    "kernelspec": {
      "display_name": "Python 3",
      "name": "python3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "nbformat": 4,
  "nbformat_minor": 0
}