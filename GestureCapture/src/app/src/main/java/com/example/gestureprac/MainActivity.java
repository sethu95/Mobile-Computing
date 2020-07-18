package com.example.gestureprac;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.Spinner;

public class MainActivity extends AppCompatActivity {
    String option;
    Spinner gestureSpinner;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        gestureSpinner = (Spinner) findViewById(R.id.gestureListSpinner);
        ArrayAdapter<String> gestureListAdapter = new ArrayAdapter<String>(MainActivity.this,
                android.R.layout.simple_list_item_1, getResources().getStringArray(R.array.gestureList));
        gestureListAdapter.setDropDownViewResource(android.R.layout.simple_dropdown_item_1line);
        gestureSpinner.setAdapter(gestureListAdapter);
        Button showVideoButton = (Button) findViewById(R.id.showVideoButton);
        showVideoButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(MainActivity.this, SecondActivity.class);
                option = gestureSpinner.getSelectedItem().toString();
                intent.putExtra("option", option);
                startActivity(intent);
            }
        });
    }
}
