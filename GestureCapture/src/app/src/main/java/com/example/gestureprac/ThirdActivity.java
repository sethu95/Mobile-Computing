package com.example.gestureprac;

import androidx.appcompat.app.AppCompatActivity;

import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
import android.os.StrictMode;
import android.provider.MediaStore;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;
import android.widget.VideoView;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.net.URL;
import java.net.URLConnection;
import java.util.HashMap;
import java.util.Map;

public class ThirdActivity extends AppCompatActivity {

    public static final int ACCESS_CODE = 101;
    public static Uri VIDEO_URI = null;
    public static String FILE_NAME = "";
    public static String USER_LAST_NAME = "MANICKAM";
    public String SIGN_NAME = "";
    public static Map<String, Integer> signFreqMap = new HashMap<String, Integer>();

    static {
        signFreqMap.put("House", 0);
        signFreqMap.put("Buy", 0);
        signFreqMap.put("Hope", 0);
        signFreqMap.put("Fun", 0);
        signFreqMap.put("Arrive", 0);
        signFreqMap.put("Really", 0);
        signFreqMap.put("Read", 0);
        signFreqMap.put("Lip", 0);
        signFreqMap.put("Mouth", 0);
        signFreqMap.put("Some", 0);
        signFreqMap.put("Communicate", 0);
        signFreqMap.put("Write", 0);
        signFreqMap.put("Create", 0);
        signFreqMap.put("Pretend", 0);
        signFreqMap.put("Sister", 0);// No Link
        signFreqMap.put("Man", 0);
        signFreqMap.put("One", 0);// No Link
        signFreqMap.put("Drive", 0);// No Link
        signFreqMap.put("Perfect", 0);
        signFreqMap.put("Mother", 0);
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_third);
        Intent intent = getIntent();
        SIGN_NAME = intent.getStringExtra("signName");
        Button viewVideoButton = (Button) findViewById(R.id.viewVideoButton);
        viewVideoButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                VideoView videoView = (VideoView) findViewById(R.id.videoView);
                if(checkSelfPermission(Manifest.permission.WRITE_EXTERNAL_STORAGE) != PackageManager.PERMISSION_GRANTED) {
                    requestPermissions(new String[]{Manifest.permission.WRITE_EXTERNAL_STORAGE}, 1);
                } else {
                    Uri uri = Uri.parse(VIDEO_URI.toString());
                    videoView.setVideoURI(uri);
                    videoView.start();
                }
            }
        });

        Button captureVideoButton = (Button) findViewById(R.id.recordButton);
        captureVideoButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                int freq = signFreqMap.get(SIGN_NAME);
                signFreqMap.put(SIGN_NAME, ++freq);
                String fileName = SIGN_NAME.toUpperCase() + "_PRACTICE_(" + signFreqMap.get(SIGN_NAME) + ")_" + USER_LAST_NAME + ".mp4";
                File gestureFile = new File(Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DCIM), "Camera");
                StrictMode.VmPolicy.Builder builder = new StrictMode.VmPolicy.Builder();
                StrictMode.setVmPolicy(builder.build());
                Intent videoIntent = new Intent(MediaStore.ACTION_VIDEO_CAPTURE);
                videoIntent.putExtra(MediaStore.EXTRA_DURATION_LIMIT, 5);
                videoIntent.putExtra(MediaStore.EXTRA_OUTPUT, Uri.fromFile(new File(gestureFile.getPath() + fileName)));
                if(videoIntent.resolveActivity(getPackageManager()) != null) {
                    startActivityForResult(videoIntent, ACCESS_CODE);
                }
                FILE_NAME = fileName;
            }
        });

        Button uploadVideoButton = (Button) findViewById(R.id.uploadButton);
        uploadVideoButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Thread thread = new Thread(new Runnable() {

                    @Override
                    public void run() {
                        try {
                            StringBuffer sb = new StringBuffer( "ftp://" );
                            sb.append( "sethu" ); // username
                            sb.append( ':' );
                            sb.append( "xyz123" ); // password
                            sb.append( '@' );
                            sb.append( "192.168.0.44" ); // FTP server URL
                            sb.append( '/' );
                            sb.append( FILE_NAME );
                            sb.append( ";type=i" );
                            BufferedInputStream bis = null;
                            BufferedOutputStream bos = null;
                            try {
                                URL url = new URL( sb.toString() );
                                URLConnection urlc = url.openConnection();
                                bos = new BufferedOutputStream( urlc.getOutputStream() );
                                bis = new BufferedInputStream( new FileInputStream(new File(VIDEO_URI.toString().substring(7)))); /* Cutting out the file:\\ */
                                int i;
                                // read byte by byte until end of stream
                                while ((i = bis.read()) != -1) {
                                    bos.write(i);
                                }
                            }
                            finally {
                                if (bis != null)
                                    try {
                                        bis.close();
                                    }
                                    catch (IOException ioe) {
                                        ioe.printStackTrace();
                                        showToast("Video upload failed");
                                    }
                                if (bos != null)
                                    try {
                                        bos.close();
                                    }
                                    catch (IOException ioe) {
                                        ioe.printStackTrace();
                                        showToast("Video upload failed");
                                    }
                            }

                        } catch (Exception e) {
                            e.printStackTrace();
                            showToast("Video upload failed");
                        } finally {
                            showToast("Video uploaded successfully");
                        }
                    }
                });
                thread.start();
                Intent goBackToMain = new Intent(ThirdActivity.this, MainActivity.class);// Go back to first screen
                startActivity(goBackToMain);
            }
        });
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        if(requestCode == ACCESS_CODE && resultCode == RESULT_OK) {
            VIDEO_URI = data.getData();
        }
    }

    public void showToast(final String toast)
    {
        ThirdActivity.this.runOnUiThread(new Runnable() {
            public void run() {
                Toast.makeText(ThirdActivity.this, toast, Toast.LENGTH_SHORT).show();
            }
        });
    }

}
