import java.util.Scanner;
// Created a public class called Football Player to contain my code
public class PlayerSelection{
    public static void main(String[] args) {
// Declaration of pound and meter constants for task 2
        double pound = 0.45359237;
        int meter = 100;
        

// Named my scanner object to take input from the system's user
        Scanner scanner = new Scanner (System.in);

// Ask for the player name
        System.out.println("Enter Player name:");
        String name = scanner.nextLine();

// Ask for the player's age
        System.out.println("Enter age:");
        int age = scanner.nextInt();

// Ask for the player's height in meters
       
        System.out.println("Enter height (metres):");
        float height = scanner.nextFloat();
// Ask for the player's weight in pounds
        
        System.out.println("Enter weight (pounds):");
        float weight = scanner.nextFloat();
    
// Ask for the player's jersey number

        System.out.println("Enter jersey number:");
        int jerseyNo = scanner.nextInt();
// for the next step, I display all the data collected from the user so far
        System.out.println("NAME: "+name+"\n"+"AGE: "+age+"\n"+"HEIGHT: "+height+"m"+"\n"+"WEIGHT: "+weight+"lbs"+"\n"+"JERSEY NUMBER: "+jerseyNo);
        System.out.println("---------------------------------------------------------");
        System.out.println("UPDATED STATS");
        System.out.println("---------------------------------------------------------");
// In task 2, I created formulae to convert height to centimetres, and the weight to kilograms
        double heightCm = height * meter;
        double weightKg = weight * pound;

        int newHeight = (int) heightCm;
        int newWeight = (int) weightKg;
// Then displayed the updated player details with height in cm and weight in kg
        System.out.println("NAME: "+name+"\n"+"AGE: "+age+"\n"+"HEIGHT IN CM: "+newHeight+" cm"+"\n"+"WEIGHT IN KG: "+newWeight+" kg"+"\n"+"JERSEY NUMBER: "+jerseyNo);
        System.out.println("---------------------------------------------------------");
//TASK 3: 
// Display the current age and add an increment of one
        System.out.println("Current age: "+age);
        int newAge = ++age;

        
// Created a condition that all players above age 35 will receive a reduction of their jersey number
        if (age > 35){
            System.out.println("Players above the age of 35 will recieve a reudction of their jersey number");
            --jerseyNo;
            System.out.println("New Jersey Number "+jerseyNo);
        }
    // Displayed the updated age and jersey number
        System.out.println("Age after season end: "+newAge);
        System.out.println("--------------------------------------------------------");

//TASK 4:
// This section of the code is to the check the eligibility status of the players
        System.out.println("ELIGIBILITY STATUS");
        System.out.println("--------------------------------------------------------");

        String eligibility;
            if (age >= 18 && age< 35 && newWeight <= 90){
                eligibility = ("ELIGIBLE");
              // if the player is 18 or older but less than 35 years old and they weigh less than 90 kg, they are eligible
            }
            else {
                eligibility = ("NOT ELIGIBLE");
             }
        //If the player is not eligible, the reasons for their ineligibility is stated either age reason or weight reasons
             if (age > 35){System.out.println("Player is too old to play");
                }
            else {
                if (age < 18){
                    System.out.println("Player is underage");
                }
                System.out.println(eligibility);
            }
            if (newWeight >= 90){
                System.out.println("Player is overweight");
            }
//I then categorize the players into three categories based on their ages
            String category = "";
            if (age < 20){
                category = ("rising star");
            }
            else {
                if (age >= 20 && age<= 30){
                    category = ("Prime player");
                    System.out.println("");
                }
            else{
                if (age > 30){
                    category = ("Veteran");
                }
            }
            }
// I then assigned the players positions based on their jersey numbers
                System.out.println("POSITION AND LINEUPS");
                System.out.println("-----------------------------------------------------------------");

//Using the switch statement and jeseyNo as the parameter, I mapped the positions to specific jersey numbers
                String position = "";
                switch (jerseyNo){

                    case 1:
                    position = ("Goalkeeper");
                    break;

                    case 2,3:
                    position = ("Fullback");
                    break;

                    case 4,5:
                    position = ("Centre-Back");
                    break;

                    case 6:
                    position = ("Defensive Midfielder");
                    break;

                    case 8:
                    position = ("Central Midfielder");
                    break;

                    case 10:
                    position = ("Attacking Midfielder");
                    break;

                    case 7,11,20:
                    position = ("Winger");
                    break;

                    case 9:
                    position = ("Striker");
                    break;

                    default:
                    System.out.println("Player position not known");

                }
    // An additional conditon was added to check if the player being profiled was an attacker based on their jersey number

                String attackerJersey = (jerseyNo == 7 || jerseyNo == 11 || jerseyNo ==9) ? "YES": "NO";
//  Created a variable finalLineup.
                String finalLineup;
// Using this, we checked if the player fits the criteria for a prime player, and if their weight is below 80kg
                if (category.equals("Prime player")){

                if (newWeight < 80){
                            finalLineup = ("STARTING LINEUP");
                        } 
// If the aforementioned conditions are met, the player is placed in the starting lineup, else the player is benched
                        else{
                            finalLineup = ("BENCHED");
                        }
                }
                else{
                    finalLineup = ("BENCH");
                }
// The last variable I created is named decision, used to represent whether a player will actually play or will rest
// I used the condition for eligibility to make the final decision using the ternary operator
                String decision = (age >= 18 && age<= 35 && newWeight <= 90)? "Play": "Rest";
                System.out.println("FINAL DECISION: "+decision);

// Finally, the various conditionals, operators and variables were brought together and displayed
// Using System.out.println, I displayed the entire player report
            System.out.println("-----------------------------------------------------------------");
            System.out.println("PLAYER REPORT");
            System.out.println("-----------------------------------------------------------------");
            System.out.println("Player: "+name);
            System.out.println("Age: "+age+" "+"("+category+")");
            System.out.println("Height: "+newHeight+"cm");
            System.out.println("Weight: "+newWeight+"kg");
            System.out.println("Jersey Number: "+jerseyNo);
            System.out.println("Position: "+position);
            System.out.println("Attacker Jersey: "+attackerJersey);
            System.out.println("Eligibility: "+eligibility);
            System.out.println("Lineup Decision:"+finalLineup);
            System.out.println("Final Decision: "+decision);
            System.out.println("");










        

 // Don't forget to close the scanner......       
scanner.close();
       


    
    }


}
