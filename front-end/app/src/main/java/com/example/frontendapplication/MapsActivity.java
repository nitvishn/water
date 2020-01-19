package com.example.frontendapplication;

import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.graphics.Color;
import android.os.Bundle;
import android.view.View;




import androidx.coordinatorlayout.widget.CoordinatorLayout;
import androidx.fragment.app.FragmentActivity;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.JsonArrayRequest;
import com.android.volley.toolbox.Volley;
import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.MarkerOptions;
import com.google.android.gms.maps.model.Polyline;
import com.google.android.gms.maps.model.PolylineOptions;
import com.google.android.material.snackbar.Snackbar;

import java.util.Calendar;
import android.app.DatePickerDialog;
import android.widget.Button;
import android.widget.DatePicker;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.URL;
import java.util.LinkedList;
import java.util.List;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import android.os.AsyncTask;
import android.os.Bundle;
import android.app.Activity;
import android.util.Log;

import com.google.maps.android.PolyUtil;



public class MapsActivity extends FragmentActivity implements OnMapReadyCallback{

    private GoogleMap mMap;
    int mYear, mMonth, mDay;
    int cYear, cMonth, cDay;
    int numTankers = 30;
    String[] tanker = new String[numTankers + 1];
    boolean[] checkedItems = new boolean[numTankers + 1];
    public boolean[] newcheckedItems = fillItems(checkedItems);
    public int count = 0;
    public boolean hasData = false;
    public JSONObject server_response;
    List<String> polyline_strings = new LinkedList<>();

    private RequestQueue mQueue;
    MarkerOptions place1, place2;

    Polyline Polyline1;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_maps);
        // Obtain the SupportMapFragment and get notified when the map is ready to be used.
        SupportMapFragment mapFragment = (SupportMapFragment) getSupportFragmentManager()
                .findFragmentById(R.id.map);
        mapFragment.getMapAsync(this);
        mQueue = Volley.newRequestQueue(this);


    }


    @Override
    public void onMapReady(GoogleMap googleMap) {
        mMap = googleMap;

        // Add a marker in Sydney and move the camera

//        mMap.addMarker(new MarkerOptions().position(adarsh).title("Adarsh Palm Retreat"));




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
                        getJson(dateToUse);
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

            }
        });

// add OK and Cancel buttons
        builder.setPositiveButton("OK", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                // user clicked OK
                mMap.clear();

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

    private void getJson(String dateToUse) {
        String url = "https://water-codefest.herokuapp.com/api?date=" + dateToUse + "&vendor_id=1";
        JsonObjectRequest request = new JsonObjectRequest(Request.Method.GET, url, null,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        server_response = response;
                        hasData = true;
                        System.out.println(server_response);
                    }
                }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                error.printStackTrace();
            }
        });
        mQueue.add(request);
    }
    public void showRoutes(View view) {
        place1 = new MarkerOptions().position(new LatLng(27.658143, 85.3199503)).title("Location 1");
        place2 = new MarkerOptions().position(new LatLng(27.667491, 85.3208583)).title("Location 2");
        mMap.addMarker(place1);
        mMap.addMarker(place2);

        double lat1 = 27.658143;
        double long1 = 85.3199503;

        double lat2 = 27.667491;
        double long2 = 85.3208583;

        String routeURL = "https://graphhopper.com/api/1/route?point=" + lat1 + "," + long1 + "&point=" + lat2 + "," + long2 + "&vehicle=car&key=9ff204aa-4358-4f48-863a-7085164d1eae";
        JsonObjectRequest request = new JsonObjectRequest(Request.Method.GET, routeURL, null,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        try {
                            polyline_strings.add(response.getJSONArray("paths").getJSONObject(0).getString("points"));
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }
        }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                error.printStackTrace();
            }
        });
        mQueue.add(request);

        for(String polyline: polyline_strings) {
            List<LatLng> line_points = PolyUtil.decode(polyline);
            for (int i = 0; i < line_points.size() - 1; i++) {
                LatLng src = line_points.get(i);
                LatLng dest = line_points.get(i + 1);

                // mMap is the Map Object
                Polyline line = mMap.addPolyline(
                        new PolylineOptions().add(
                                new LatLng(src.latitude, src.longitude),
                                new LatLng(dest.latitude,dest.longitude)
                        ).width(2).color(Color.BLUE).geodesic(true)
                );
            }
        }

//
//        new com.example.frontendapplication.FetchURL(MapsActivity.this).execute(getUrl(place1.getPosition(), place2.getPosition(), "driving"), "driving");
//        if(!hasData){
//            return;
//        }
//        for(int tanker_index = 1; tanker_index <= numTankers; tanker_index++){
//            if(!checkedItems[tanker_index]) {
//                continue;
//            }
//            try{
//                JSONArray tanker = server_response.getJSONArray("data").getJSONArray(tanker_index-1);
//                for(int location_index = 0; location_index < tanker.length(); location_index++){
//                    try{
//                        JSONObject location = tanker.getJSONObject(location_index);
//                        //draw the point
//                        String name = location.getString("name");
//                        double xcoord = location.getDouble("x");
//                        double ycoord = location.getDouble("y");
//                        String type = location.getString("type");
//                        String locality = location.getString("locality");
//                        int vendor_id = location.getInt("vendor_id");
//                        double tanker_supply_factor = location.getDouble("tanker_supply_factor");
//                        double consumption = location.getDouble("consumption");
//                        LatLng point = new LatLng(xcoord, ycoord);
//                        mMap.addMarker(new MarkerOptions().position(point).title(locality));
//                        System.out.println(xcoord);
//                        System.out.println(ycoord);
//
//                    }catch(JSONException e){
//                        e.printStackTrace();
//                        continue;
//                    }
//                }
//            }catch(JSONException e){
//                e.printStackTrace();
//                continue;
//            }
//        }
    }
}



