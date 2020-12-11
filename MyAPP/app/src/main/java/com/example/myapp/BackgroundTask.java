package com.example.myapp;
import android.os.AsyncTask;

import java.io.DataOutputStream;
import java.io.IOException;
import java.net.Socket;
public class BackgroundTask extends AsyncTask<String, Void, Void> {
    Socket s;
    DataOutputStream dos;
    String ip, message, message2;

    @Override
    protected Void doInBackground(String... params) {
        ip = "179.14.251.47";
        //179.14.251.47
        message = params[0];
        message2 = params[1];

        try {
            s = new Socket(ip, 8080);
            dos = new DataOutputStream(s.getOutputStream());
            System.out.println("Se ha enviado info");
            dos.writeUTF(message);
            dos.writeUTF(message2);
            dos.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
        return null;
    }
}
