import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material

ApplicationWindow{
    visible: true
    width: 500
    height: 400
    Material.theme: 'Dark'
    font.pixelSize: 24

    Row {
        id: header_row
        spacing: 20
        anchors {
            horizontalCenter: parent.horizontalCenter
            top: parent.top
            topMargin: 20
        }

        TextField {
            id: in_name
            placeholderText: 'Seu nome'
            width: 200  
        }
        
        TextField {
            id: in_server
            placeholderText: 'IP do servidor'
            width: 200  
        }
        
        TextField {
            id: in_port
            placeholderText: 'Porta'
            width: 200  
        }

        Button{
            text: 'Conectar'
            width: 150
            onClicked:{
                /* Javascript */
                ponte.connect_to_server(name=in_name.text, server=in_server.text, port=in_port.text)
                //status.text = fetch_return
            }
        }

        Label {
            id: status
            text: ''
        }
    }



    Row {
        id: main_content
        spacing: 20
    
        anchors {
            horizontalCenter: parent.horizontalCenter
            top: header_row.top
            topMargin: 60
        }

        Rectangle {
            width: maximumWidth
            height: 300
            color: "gray"
            radius: 10
            ScrollView {
                id: view
                anchors.fill: parent

                TextArea {
                    text: "TextArea\n...\n...\n...\n...\n...dasdasdasdsadsada\n...\n"
                }
            }
        }
    
        Rectangle {
            width: maximumWidth
            height: 300
            color: "orange"
            radius: 10
            Column {
                CheckBox  {
                    checked: true
                    text: qsTr("First")
                }
                CheckBox   {
                    text: qsTr("Second")
                }
                CheckBox  {
                    text: qsTr("Third")
                }
            }
        }
    }

    //Label {
    //    id: label
    //    text: 'Pokemon!'
    //    anchors {
    //        horizontalCenter: parent.horizontalCenter
    //        top: row.top
    //        topMargin: 60
    //    }
    //}


    //TextArea {
    //    id: show_text
    //    anchors {
    //        //horizontalCenter: parent.horizontalCenter
    //        top: header_row.top
    //        horizontalCenter: parent.horizontalCenter
    //        topMargin: 60
    //    }
    //
    //    placeholderText: qsTr("Mensagens recebidas")
    //}

    Row {
        id: botton_line
        spacing: 20
        anchors {
            horizontalCenter: parent.horizontalCenter
            top: main_content.bottom
            topMargin: 50
        }

        TextField {
            id: text_msg
            width: 600
            placeholderText: 'Mensagem'
        }
        
        Button{
            text: 'Enviar'
            width: 150
            onClicked:{
                /* Javascript */
                var fetch_return = ponte.fetch_image(pokemon_id.text)
                pokemon_id.text = ''
                img.source = ''
                label.text = fetch_return[1]
                img.source = fetch_return[0]
            }
        }
    }



}

