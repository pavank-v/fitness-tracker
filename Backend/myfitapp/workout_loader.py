import os
import sys
import django

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')

# Initialize Django
django.setup()

from myfitapp.models import (
    CardioTraining,
    CrossFitTraining,
    FlexibilityTraining,
    MuscleGroup,
    Recovery,
    ResistanceTraining,
)


# Function to add the Resistance workouts to database
def add_resistance_workouts():
    exercises = {
        "Beginner": {
            "Chest": [
                {
                    "name": "Machine Chest Press",
                    "sets": 3,
                    "reps": "10 - 15",
                    "weight": "20kg to 40 kg",
                },
                {
                    "name": "Smith Machine Incline Press",
                    "sets": 3,
                    "reps": "10 - 15",
                    "weight": "20kg to 40 kg",
                },
                {
                    "name": "Cable Flies",
                    "sets": 3,
                    "reps": "10 - 15",
                    "weight": "10kg to 15 kg",
                },
            ],
            "Back": [
                {
                    "name": "Lat Pulldown",
                    "sets": 3,
                    "reps": "10 - 15",
                    "weight": "30kg to 40 kg",
                },
                {
                    "name": "Horizontal Cable Row",
                    "sets": 3,
                    "reps": "10 - 15",
                    "weight": "20kg to 40 kg",
                },
                {
                    "name": "Shrugs",
                    "sets": 3,
                    "reps": "10 - 15",
                    "weight": "25kg to 40 kg",
                },
            ],
            "Legs": [
                {
                    "name": "Smith Machine Squats",
                    "sets": 3,
                    "reps": "10 - 15",
                    "weight": "30kg to 40 kg",
                },
                {
                    "name": "Leg Curls",
                    "sets": 3,
                    "reps": "10 - 15",
                    "weight": "20kg to 40 kg",
                },
                {
                    "name": "Calf Raises",
                    "sets": 3,
                    "reps": "10 - 15",
                    "weight": "25kg to 40 kg",
                },
            ],
            "Shoulders": [
                {
                    "name": "Shoulder Dumbbell Press",
                    "sets": 3,
                    "reps": "10 - 15",
                    "weight": "15kg to 25 kg",
                },
                {
                    "name": "Lateral Raises",
                    "sets": 3,
                    "reps": "10 - 15",
                    "weight": "5kg to 15 kg",
                },
                {
                    "name": "Face Pulls",
                    "sets": 3,
                    "reps": "10 - 15",
                    "weight": "10kg to 20 kg",
                },
            ],
            "Arms": [
                {
                    "name": "Barbell Curls",
                    "sets": 3,
                    "reps": "10 - 15",
                    "weight": "15kg to 25 kg",
                },
                {
                    "name": "Skull Crushers",
                    "sets": 3,
                    "reps": "10 - 15",
                    "weight": "15kg to 25 kg",
                },
                {
                    "name": "Tricep Extensions",
                    "sets": 3,
                    "reps": "10 - 15",
                    "weight": "10kg to 20 kg",
                },
                {
                    "name": "Hammer Curls",
                    "sets": 3,
                    "reps": "10 - 15",
                    "weight": "10kg to 20 kg",
                },
                {
                    "name": "Wrist Extensions",
                    "sets": 3,
                    "reps": "10 - 15",
                    "weight": "10kg to 20 kg",
                },
                {
                    "name": "Wrist Flexions",
                    "sets": 3,
                    "reps": "10 - 15",
                    "weight": "10kg to 20 kg",
                },
            ],
        },
        "Intermediate": {
            "Chest": [
                {
                    "name": "Incline Dumbbell Press",
                    "sets": 4,
                    "reps": "8 - 12",
                    "weight": "25kg to 40kg",
                },
                {
                    "name": "Flat Bench Dumbbell Fly",
                    "sets": 4,
                    "reps": "8 - 12",
                    "weight": "15kg to 25kg",
                },
                {
                    "name": "Cable Crossover",
                    "sets": 4,
                    "reps": "8 - 12",
                    "weight": "10kg to 20kg",
                },
            ],
            "Back": [
                {
                    "name": "T-Bar Row",
                    "sets": 4,
                    "reps": "8 - 12",
                    "weight": "40kg to 60kg",
                },
                {
                    "name": "Single-Arm Dumbbell Row",
                    "sets": 4,
                    "reps": "8 - 12",
                    "weight": "25kg to 40kg",
                },
                {
                    "name": "Deadlift",
                    "sets": 4,
                    "reps": "6 - 8",
                    "weight": "60kg to 100kg",
                },
            ],
            "Legs": [
                {
                    "name": "Front Squats",
                    "sets": 4,
                    "reps": "8 - 12",
                    "weight": "40kg to 60kg",
                },
                {
                    "name": "Romanian Deadlifts",
                    "sets": 4,
                    "reps": "8 - 12",
                    "weight": "40kg to 60kg",
                },
                {
                    "name": "Leg Press",
                    "sets": 4,
                    "reps": "8 - 12",
                    "weight": "100kg to 150kg",
                },
            ],
            "Shoulders": [
                {
                    "name": "Arnold Press",
                    "sets": 4,
                    "reps": "8 - 12",
                    "weight": "15kg to 25kg",
                },
                {
                    "name": "Cable Lateral Raises",
                    "sets": 4,
                    "reps": "8 - 12",
                    "weight": "5kg to 15kg",
                },
                {
                    "name": "Face Pulls",
                    "sets": 4,
                    "reps": "8 - 12",
                    "weight": "10kg to 20kg",
                },
            ],
            "Arms": [
                {
                    "name": "Preacher Curls",
                    "sets": 4,
                    "reps": "8 - 12",
                    "weight": "15kg to 25kg",
                },
                {
                    "name": "Overhead Tricep Extension",
                    "sets": 4,
                    "reps": "8 - 12",
                    "weight": "10kg to 20kg",
                },
                {
                    "name": "Concentration Curls",
                    "sets": 4,
                    "reps": "8 - 12",
                    "weight": "10kg to 15kg",
                },
            ],
        },
        "Advance": {
            "Chest": [
                {
                    "name": "Barbell Bench Press",
                    "sets": 5,
                    "reps": "6 - 8",
                    "weight": "60kg to 100kg",
                },
                {
                    "name": "Incline Barbell Press",
                    "sets": 5,
                    "reps": "6 - 8",
                    "weight": "60kg to 100kg",
                },
                {
                    "name": "Weighted Dips",
                    "sets": 5,
                    "reps": "6 - 8",
                    "weight": "10kg to 20kg",
                },
            ],
            "Back": [
                {
                    "name": "Bent-Over Rows",
                    "sets": 5,
                    "reps": "6 - 8",
                    "weight": "60kg to 100kg",
                },
                {
                    "name": "Weighted Pull-Ups",
                    "sets": 5,
                    "reps": "6 - 8",
                    "weight": "10kg to 20kg",
                },
                {
                    "name": "Deficit Deadlift",
                    "sets": 5,
                    "reps": "4 - 6",
                    "weight": "80kg to 120kg",
                },
            ],
            "Legs": [
                {
                    "name": "Barbell Back Squat",
                    "sets": 5,
                    "reps": "6 - 8",
                    "weight": "80kg to 120kg",
                },
                {
                    "name": "Walking Lunges",
                    "sets": 5,
                    "reps": "12 steps",
                    "weight": "30kg to 50kg",
                },
                {
                    "name": "Seated Calf Raise",
                    "sets": 5,
                    "reps": "8 - 12",
                    "weight": "40kg to 60kg",
                },
            ],
            "Shoulders": [
                {
                    "name": "Seated Barbell Press",
                    "sets": 5,
                    "reps": "6 - 8",
                    "weight": "40kg to 60kg",
                },
                {
                    "name": "Reverse Pec Deck Fly",
                    "sets": 5,
                    "reps": "6 - 8",
                    "weight": "15kg to 25kg",
                },
                {
                    "name": "Upright Row",
                    "sets": 5,
                    "reps": "6 - 8",
                    "weight": "20kg to 40kg",
                },
            ],
            "Arms": [
                {
                    "name": "Spider Curls",
                    "sets": 5,
                    "reps": "6 - 8",
                    "weight": "15kg to 25kg",
                },
                {
                    "name": "Close-Grip Bench Press",
                    "sets": 5,
                    "reps": "6 - 8",
                    "weight": "40kg to 60kg",
                },
                {
                    "name": "Reverse Grip Tricep Pushdown",
                    "sets": 5,
                    "reps": "6 - 8",
                    "weight": "10kg to 20kg",
                },
            ],
        },
    }

    for level_name, muscle_group in exercises.items():
        
        for muscle_group_name, exercises_list in muscle_group.items():
            muscle_group, _ = MuscleGroup.objects.get_or_create(name=muscle_group_name)

            for exercise in exercises_list:
                ResistanceTraining.objects.create(
                    exercise_name=exercise["name"],
                    sets=exercise["sets"],
                    reps=exercise["reps"],
                    weight=exercise["weight"],
                    muscle_group=muscle_group,
                    current_level=level_name,
                )
    print("Resistance Exercises Added Successfully!!!")


# Function to add Cardio workouts to database
def add_cardio_workouts():
    cardio_exercises = {
        "Beginner": {
            "Treadmill": [
                {"name": "Walking", "duration": 30, "intensity": "Low"},
                {"name": "Light Jogging", "duration": 20, "intensity": "Moderate"},
            ],
            "Cycling": [
                {"name": "Stationary Cycling", "duration": 25, "intensity": "Low"},
                {"name": "Outdoor Cycling", "duration": 20, "intensity": "Moderate"},
            ],
            "Bodyweight": [
                {"name": "Jumping Jacks", "duration": 10, "intensity": "Moderate"},
                {"name": "Step-Ups", "duration": 15, "intensity": "Low"},
            ],
        },
        "Intermediate": {
            "Treadmill": [
                {"name": "Interval Jogging", "duration": 30, "intensity": "Moderate"},
                {"name": "Steady Jogging", "duration": 25, "intensity": "Moderate"},
            ],
            "Cycling": [
                {"name": "Hill Cycling", "duration": 30, "intensity": "Moderate"},
                {"name": "Interval Cycling", "duration": 20, "intensity": "High"},
            ],
            "Bodyweight": [
                {"name": "Burpees", "duration": 15, "intensity": "High"},
                {"name": "Mountain Climbers", "duration": 15, "intensity": "High"},
            ],
        },
        "Advance": {
            "Treadmill": [
                {"name": "Sprinting Intervals", "duration": 30, "intensity": "High"},
                {"name": "Incline Running", "duration": 25, "intensity": "High"},
            ],
            "Cycling": [
                {
                    "name": "Long-Distance Cycling",
                    "duration": 45,
                    "intensity": "Moderate",
                },
                {"name": "HIIT Cycling", "duration": 20, "intensity": "High"},
            ],
            "Bodyweight": [
                {"name": "Jump Squats", "duration": 20, "intensity": "High"},
                {"name": "High-Intensity Burpees", "duration": 15, "intensity": "High"},
            ],
        },
    }

    for level_name, categories in cardio_exercises.items():
        for category_name, exercises in categories.items():
            for exercise in exercises:
                CardioTraining.objects.create(
                    exercise_name=exercise["name"],
                    duration=exercise["duration"],
                    intensity=exercise["intensity"],
                    current_level=level_name,
                )

    print("Cardio Workouts Loaded Successfully")


# Function to add crossfit workouts to database
def add_crossfit_workouts():
    crossfit_workouts = {
        "Beginner": [
            {"name": "Air Squats and Push-Ups", "round": 3, "time_cap": 10},
            {"name": "Burpees and Sit-Ups", "round": 3, "time_cap": 12},
            {"name": "Jump Rope and Lunges", "round": 3, "time_cap": 10},
            {"name": "Dumbbell Deadlifts and Ring Rows", "round": 4, "time_cap": 12},
            {"name": "Plank Holds and Step-Ups", "round": 3, "time_cap": 10},
            {"name": "Kettlebell Deadlifts and Push Press", "round": 3, "time_cap": 15},
        ],
        "Intermediate": [
            {"name": "Wall Balls and Pull-Ups", "round": 5, "time_cap": 15},
            {"name": "Kettlebell Swings and Box Jumps", "round": 4, "time_cap": 12},
            {"name": "Overhead Press and Deadlifts", "round": 4, "time_cap": 15},
            {"name": "Rowing and Dumbbell Snatches", "round": 4, "time_cap": 18},
            {"name": "Thrusters and Toes-to-Bar", "round": 5, "time_cap": 16},
            {
                "name": "Burpee Box Jump Overs and Power Cleans",
                "round": 4,
                "time_cap": 18,
            },
        ],
        "Advance": [
            {"name": "Snatches and Muscle-Ups", "round": 6, "time_cap": 20},
            {"name": "Clean and Jerks with Double Unders", "round": 5, "time_cap": 18},
            {"name": "Thrusters and Chest-to-Bar Pull-Ups", "round": 5, "time_cap": 20},
            {"name": "Overhead Squats and Rope Climbs", "round": 5, "time_cap": 22},
            {
                "name": "Barbell Complex (Clean, Front Squat, Jerk)",
                "round": 5,
                "time_cap": 20,
            },
            {"name": "Deadlifts and Handstand Push-Ups", "round": 6, "time_cap": 18},
            {
                "name": "Sprint Intervals and Ring Muscle-Ups",
                "round": 6,
                "time_cap": 25,
            },
        ],
    }

    for level_name, exercises_list in crossfit_workouts.items():
        for exercise in exercises_list:
            CrossFitTraining.objects.create(
                exercise_name=exercise["name"],
                rounds=exercise["round"],
                time_cap=exercise["time_cap"],
                current_level=level_name,
            )

    print("Crossfit Workouts Loaded Successfully")


# Function to add Flexibility Workouts to database
def add_flexibility_workouts():
    flexibility_workouts = {
        "Beginner": [
            {"name": "Seated Forward Bend", "duration": 60, "stretch_type": "Static"},
            {"name": "Cat-Cow Stretch", "duration": 30, "stretch_type": "Dynamic"},
            {"name": "Standing Hamstring Stretch", "duration": 60, "stretch_type": "Static"},
            {"name": "Side Neck Stretch", "duration": 30, "stretch_type": "Static"},
            {"name": "Ankle Circles", "duration": 30, "stretch_type": "Dynamic"},
            {"name": "Child's Pose", "duration": 60, "stretch_type": "Static"},
        ],
        "Intermediate": [
            {"name": "Side Lunge Stretch", "duration": 30, "stretch_type": "Dynamic"},
            {"name": "Butterfly Stretch", "duration": 60, "stretch_type": "Static"},
            {"name": "Thread the Needle", "duration": 45, "stretch_type": "Static"},
            {"name": "Dynamic Torso Twists", "duration": 30, "stretch_type": "Dynamic"},
            {"name": "Hip Flexor Stretch", "duration": 60, "stretch_type": "Static"},
            {"name": "Chest Opener Stretch", "duration": 60, "stretch_type": "Static"},
        ],
        "Advanced": [
            {"name": "World's Greatest Stretch", "duration": 45, "stretch_type": "Dynamic"},
            {"name": "Spinal Twists", "duration": 45, "stretch_type": "Static"},
            {"name": "Cobra Stretch", "duration": 60, "stretch_type": "Static"},
            {"name": "Wrist Circles", "duration": 30, "stretch_type": "Dynamic"},
            {"name": "Hamstring PNF Stretch", "duration": 60, "stretch_type": "Static"},
            {"name": "Standing Quad Stretch", "duration": 60, "stretch_type": "Static"},
            {"name": "Overhead Shoulder Stretch", "duration": 45, "stretch_type": "Static"},
        ],
    }

    for level, stretches_list in flexibility_workouts.items():
        for stretch in stretches_list:
            FlexibilityTraining.objects.create(
                exercise_name=stretch["name"],
                duration=stretch["duration"],
                stretch_type=stretch["stretch_type"],
                current_level=level, 
            )

    print("Flexibility Workouts Loaded Successfully")

# Function to add Recovery Workouts to database
def add_recovery_methods():
    recovery_workouts = {
        "Beginner": [
            {"name": "Foam Rolling", "duration": 10, "recovery_type": "Active"},
            {"name": "Massage Therapy", "duration": 30, "recovery_type": "Passive"},
            {"name": "Hydration Breaks", "duration": 5, "recovery_type": "Passive"},
            {"name": "Gentle Stretching", "duration": 10, "recovery_type": "Active"},
            {"name": "Breathing Exercises", "duration": 5, "recovery_type": "Psychological"},
            {"name": "Progressive Muscle Relaxation", "duration": 15, "recovery_type": "Psychological"},
        ],
        "Intermediate": [
            {"name": "Yoga Nidra", "duration": 20, "recovery_type": "Psychological"},
            {"name": "Cold Water Immersion", "duration": 15, "recovery_type": "Passive"},
            {"name": "Contrast Showers", "duration": 10, "recovery_type": "Passive"},
            {"name": "Active Stretching", "duration": 10, "recovery_type": "Active"},
            {"name": "Gentle Cycling", "duration": 15, "recovery_type": "Active"},
            {"name": "Mindfulness Journaling", "duration": 10, "recovery_type": "Psychological"},
        ],
        "Advanced": [
            {"name": "Hot Tub Soak", "duration": 15, "recovery_type": "Passive"},
            {"name": "Deep Tissue Massage", "duration": 30, "recovery_type": "Passive"},
            {"name": "Meditation", "duration": 15, "recovery_type": "Psychological"},
            {"name": "High-Intensity Foam Rolling", "duration": 10, "recovery_type": "Active"},
            {"name": "Sleep Optimization", "duration": 480, "recovery_type": "Psychological"},
            {"name": "Sprint Intervals for Recovery", "duration": 5, "recovery_type": "Active"},
            {"name": "Guided Visualization", "duration": 15, "recovery_type": "Psychological"},
        ],
    }

    for level, recovery_list in recovery_workouts.items():
        for recovery in recovery_list:
            Recovery.objects.create(
                method_name=recovery["name"],
                duration=recovery["duration"],
                recovery_type=recovery["recovery_type"],
                current_level=level,  
            )

    print("Recovery Methods Loaded Successfully")


add_resistance_workouts()
add_cardio_workouts()
add_recovery_methods()
add_crossfit_workouts()
add_flexibility_workouts()