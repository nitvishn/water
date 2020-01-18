package com.example.frontendapplication;

import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.os.Bundle;
import android.view.View;


import androidx.fragment.app.FragmentActivity;

import com.android.volley.Request;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.MarkerOptions;

import java.util.Calendar;
import android.app.DatePickerDialog;
import android.widget.Button;
import android.widget.DatePicker;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.URL;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import android.os.AsyncTask;
import android.os.Bundle;
import android.app.Activity;
import android.util.Log;


public class MapsActivity extends FragmentActivity implements OnMapReadyCallback {

    private GoogleMap mMap;
    int mYear, mMonth, mDay;
    int cYear, cMonth, cDay;
    String[] tanker = new String[31];
    boolean[] checkedItems = new boolean[31];
    public boolean[] newcheckedItems = fillItems(checkedItems);
    public int count = 0;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_maps);
        // Obtain the SupportMapFragment and get notified when the map is ready to be used.
        SupportMapFragment mapFragment = (SupportMapFragment) getSupportFragmentManager()
                .findFragmentById(R.id.map);
        mapFragment.getMapAsync(this);
    }


    @Override
    public void onMapReady(GoogleMap googleMap) {
        mMap = googleMap;

        // Add a marker in Sydney and move the camera
        LatLng adarsh = new LatLng(12.922770, 77.694033);
        mMap.addMarker(new MarkerOptions().position(adarsh).title("Adarsh Palm Retreat"));
        mMap.moveCamera(CameraUpdateFactory.newLatLng(adarsh));
        mMap.moveCamera(CameraUpdateFactory.zoomTo(16.0f));


    }

    public void selectDate(View view) {
        final Button dateButton = (Button) findViewById(R.id.date_button);
        final Calendar c = Calendar.getInstance();
        mYear = c.get(Calendar.YEAR);
        mMonth = c.get(Calendar.MONTH);
        mDay = c.get(Calendar.DAY_OF_MONTH);

        DatePickerDialog datePickerDialog = new DatePickerDialog(this,
                new DatePickerDialog.OnDateSetListener() {
                    public void onDateSet(DatePicker view, int year,
                                          int monthOfYear, int dayOfMonth) {
                        cYear = year;
                        cMonth = monthOfYear + 1;
                        cDay = dayOfMonth;
                        String dateToUse = dayOfMonth + "-" + (monthOfYear + 1) + "-" + year;
                        dateButton.setText(dateToUse);

                    }
                }, mYear, mMonth, mDay);
        datePickerDialog.show();
    }

    public void selectTankers(View view) {
        final Button tankerButton = (Button) findViewById(R.id.tanker_button);
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setTitle("Choose some animals");
// add a checkbox list
        String[] tankerList = tanker;
        tankerList[0] = "Choose All";
        for (int i = 1; i < 31; i++) {
            tankerList[i] = "Tanker" + Integer.toString(i);
        }
        builder.setMultiChoiceItems(tankerList, newcheckedItems, new DialogInterface.OnMultiChoiceClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which, boolean isChecked) {
                // user checked or unchecked a box
                if (which == 0 && isChecked) {
                    for (int i = 1; i < 31; i++) {
                        newcheckedItems[i] = true;
                        count++;
                    }
                } else if (which == 0 && !isChecked) {
                    for (int i = 1; i < 31; i++) {
                        newcheckedItems[i] = false;
                        count--;
                    }
                } else if (isChecked) {
                    newcheckedItems[which] = true;
                    count++;
                } else {
                    newcheckedItems[which] = false;
                    count--;
                }
                System.out.println(newcheckedItems[which]);
                if (count > 0) {
                    tankerButton.setText("Selected");
                } else {
                    tankerButton.setText("Tanker");
                }
            }
        });

// add OK and Cancel buttons
        builder.setPositiveButton("OK", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                // user clicked OK


            }
        });
        builder.setNegativeButton("Cancel", null);

// create and show the alert dialog
        AlertDialog dialog = builder.create();
        dialog.show();
    }

    public boolean[] fillItems(boolean[] arrays) {
        for (int i = 0; i < arrays.length; i++) {
            arrays[i] = false;
        }
        return arrays;
    }

    public void getJson(View view) {
        final Button dataButton = (Button) findViewById(R.id.getdata_button);
        String url = "http://my-json-feed";

        JsonObjectRequest jsonObjectRequest = new JsonObjectRequest
                (Request.Method.GET, url, null, new Response.Listener<JSONObject>() {

                    @Override
                    public void onResponse(JSONObject response) {
                        dataButton.setText("Response: " + response.toString());
                        System.out.println(response.toString());
                    }
                }, new Response.ErrorListener() {

                    @Override
                    public void onErrorResponse(VolleyError error) {
                        // TODO: Handle error

                    }
                });

// Access the RequestQueue through your singleton class.
        MySingleton.getInstance(this).addToRequestQueue(jsonObjectRequest);
    }
}


