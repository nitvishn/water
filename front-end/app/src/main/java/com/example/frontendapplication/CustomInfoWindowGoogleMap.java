package com.example.frontendapplication;

import android.app.Activity;
import android.content.Context;
import android.view.View;
import android.widget.TextView;

import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.model.Marker;

public class CustomInfoWindowGoogleMap implements GoogleMap.InfoWindowAdapter {

    private Context context;

    public CustomInfoWindowGoogleMap(Context ctx){
        context = ctx;
    }

    @Override
    public View getInfoWindow(Marker marker) {
        return null;
    }

    @Override
    public View getInfoContents(Marker marker) {
        View view = ((Activity)context).getLayoutInflater()
                .inflate(R.layout.map_custom_infowindow, null);

        TextView order = view.findViewById(R.id.order);
        TextView name = view.findViewById(R.id.name);

        TextView type = view.findViewById(R.id.type);
        TextView consumption = view.findViewById(R.id.consumption);


        order.setText(marker.getTitle());

        InfoWindowData infoWindowData = (InfoWindowData) marker.getTag();



        name.setText(infoWindowData.getName());
        type.setText(infoWindowData.getType());
        consumption.setText(infoWindowData.getConsumption());

        return view;
    }
}