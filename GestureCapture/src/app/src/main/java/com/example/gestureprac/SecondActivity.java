package com.example.gestureprac;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.MediaController;
import android.widget.VideoView;

import java.util.HashMap;
import java.util.Map;

public class SecondActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_second);
        Intent intent = getIntent();
        String option = intent.getStringExtra("option");
        final String op = option;
        Map<String, String> optionMap= new HashMap<String, String>();
        optionMap.put("House", "https://www.signingsavvy.com/media/mp4-ld/23/23234.mp4");
        optionMap.put("Buy", "https://www.signingsavvy.com/media/mp4-ld/6/6442.mp4");
        optionMap.put("Hope", "https://www.signingsavvy.com/media/mp4-ld/22/22197.mp4");
        optionMap.put("Fun", "https://www.signingsavvy.com/media/mp4-ld/22/22976.mp4");
        optionMap.put("Arrive", "https://www.signingsavvy.com/media/mp4-ld/26/26971.mp4");
        optionMap.put("Really", "https://www.signingsavvy.com/media/mp4-ld/24/24977.mp4");
        optionMap.put("Read", "https://www.signingsavvy.com/media/mp4-ld/7/7042.mp4");
        optionMap.put("Lip", "https://www.signingsavvy.com/media/mp4-ld/26/26085.mp4");
        optionMap.put("Mouth", "https://www.signingsavvy.com/media/mp4-ld/22/22188.mp4");
        optionMap.put("Some", "https://www.signingsavvy.com/media/mp4-ld/23/23931.mp4");
        optionMap.put("Communicate", "https://www.signingsavvy.com/media/mp4-ld/22/22897.mp4");
        optionMap.put("Write", "https://www.signingsavvy.com/media/mp4-ld/27/27923.mp4");
        optionMap.put("Create", "https://www.signingsavvy.com/media/mp4-ld/22/22337.mp4");
        optionMap.put("Pretend", "https://www.signingsavvy.com/media/mp4-ld/25/25901.mp4");
        optionMap.put("Sister", "https://www.signingsavvy.com/media/mp4-ld/21/21587.mp4");
        optionMap.put("Man", "https://www.signingsavvy.com/media/mp4-ld/21/21568.mp4");
        optionMap.put("One", "https://www.signingsavvy.com/media/mp4-ld/26/26492.mp4");
        optionMap.put("Drive", "https://www.signingsavvy.com/media/mp4-ld/23/23918.mp4");
        optionMap.put("Perfect", "https://www.signingsavvy.com/media/mp4-ld/24/24791.mp4");
        optionMap.put("Mother", "https://www.signingsavvy.com/media/mp4-ld/21/21571.mp4");

        VideoView gestureVideoView = (VideoView) findViewById(R.id.gestureVideoView);
        String videoPath = optionMap.get(option);
        Uri uri = Uri.parse(videoPath);
        gestureVideoView.setVideoURI(uri);
        MediaController gestureMediaController = new MediaController(this);
        gestureVideoView.setMediaController(gestureMediaController);
        gestureMediaController.setAnchorView(gestureVideoView);
        gestureMediaController.setMediaPlayer(gestureVideoView);
        gestureVideoView.start();

        Button practiceButton = (Button) findViewById(R.id.practiceGestureButton);
        practiceButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(SecondActivity.this, ThirdActivity.class);
                intent.putExtra("signName", op);
                startActivity(intent);
            }
        });

    }
}
