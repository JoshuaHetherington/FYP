/*   
    Copyright (C) 2017 ApPeAL Group, Politecnico di Torino

    This file is part of TraCI4J.

    TraCI4J is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    TraCI4J is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with TraCI4J.  If not, see <http://www.gnu.org/licenses/>.
*/

package it.polito.appeal.traci.examples;

import it.polito.appeal.traci.SumoTraciConnection;
import it.polito.appeal.traci.Vehicle;

import java.util.Collection;

public class Practice {
	
	public static void main(String []args){
		SumoTraciConnection conn = new SumoTraciConnection(
				"test/resources/sumo_maps/josh/josh.sumo.cfg",  // config file
				12345                                  // random seed
				);
		try{
			conn.runServer();
			int timeTotal = 1000;
			for(int i = 0; i < timeTotal; i++){
				int time = conn.getCurrentSimTime() / 1000;
				
				//conn.queryAddVehicle();
				//conn.queryAddVehicle();
				
				Collection<Vehicle> vehicles = conn.getVehicleRepository().getAll().values();
				java.awt.Color c = java.awt.Color.RED;
				if(vehicles.iterator().hasNext()){
					Vehicle v = vehicles.iterator().next();
					v.changeColor(c);
				}
				
				
				
				System.out.println("At time step " + time + ", there are "
						+ vehicles.size() + " vehicles: " + vehicles);
				
				conn.nextSimStep();
			}
			conn.close();
		}
		catch(Exception e) {
			e.printStackTrace();
		}
	}
}
