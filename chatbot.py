import google.generativeai as genai
from flask import current_app
import os
from datetime import datetime
from app import db
from models import Room, Hostel, Complaint, Payment, User

class HostelChatbot:
    def __init__(self):
        # Initialize Gemini API
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        self.model = genai.GenerativeModel('gemini-pro')
        
        # System prompt to define chatbot behavior with specific hostel information
        self.system_prompt = """You are a helpful hostel management assistant for IST Smart Hostel. Here is the specific information about our hostel:

Hostel Information:
- Location: IST Campus, Islamabad
- Contact: +92-123-4567890
- Email: hostel@ist.edu.pk

Room Types and Pricing:
- Single Room: $500 per semester
- Double Room: $400 per semester per person
- Triple Room: $300 per semester per person

Facilities:
- 24/7 Security
- High-speed WiFi
- Laundry Service
- Common Room
- Study Room
- Mess Facility

Rules and Regulations:
- Curfew Time: 11:00 PM
- Visitors allowed only during 2:00 PM - 7:00 PM
- No smoking in rooms
- Maintain cleanliness
- Report maintenance issues promptly

You can help with:
1. Room booking and availability queries
2. Complaint submission and tracking
3. Payment information
4. General hostel information
5. Student profile management

Always be polite and professional. If you don't know something, say so.
Keep responses concise and to the point."""
        
        # Initialize chat history
        self.chat = self.model.start_chat(history=[])
        
    def get_response(self, user_input, user_context=None):
        """
        Get response from the chatbot
        user_context: Dictionary containing user information if available
        """
        try:
            # Add context if available
            if user_context:
                context_str = f"User Context: {user_context}\n"
                prompt = f"{self.system_prompt}\n{context_str}User: {user_input}"
            else:
                prompt = f"{self.system_prompt}\nUser: {user_input}"
            
            # Get response from Gemini
            response = self.chat.send_message(prompt)
            return response.text
            
        except Exception as e:
            current_app.logger.error(f"Chatbot error: {str(e)}")
            return "I apologize, but I'm having trouble processing your request right now. Please try again later."

    def get_room_availability(self, hostel_id=None):
        """Get room availability information"""
        try:
            query = Room.query.filter_by(is_available=True)
            if hostel_id:
                query = query.filter_by(hostel_id=hostel_id)
            
            available_rooms = query.all()
            
            if not available_rooms:
                return "No rooms are currently available."
            
            response = "Available rooms:\n"
            for room in available_rooms:
                hostel = Hostel.query.get(room.hostel_id)
                response += f"- Room {room.room_number} in {hostel.name} ({room.room_type})\n"
                response += f"  Fee: ${room.fee_per_semester} per semester\n"
                response += f"  Capacity: {room.capacity} person(s)\n"
            
            return response
            
        except Exception as e:
            current_app.logger.error(f"Error getting room availability: {str(e)}")
            return "I'm having trouble checking room availability. Please try again later."

    def get_complaint_status(self, complaint_id):
        """Get status of a specific complaint"""
        try:
            complaint = Complaint.query.get(complaint_id)
            if not complaint:
                return "Complaint not found."
            
            return f"""Complaint Details:
Title: {complaint.title}
Category: {complaint.category}
Status: {complaint.status}
Created: {complaint.created_at}
Last Updated: {complaint.updated_at}
Description: {complaint.description}
Admin Notes: {complaint.admin_notes if complaint.admin_notes else 'No admin notes yet'}"""
            
        except Exception as e:
            current_app.logger.error(f"Error getting complaint status: {str(e)}")
            return "I'm having trouble checking the complaint status. Please try again later."

    def get_payment_info(self, user_id):
        """Get payment information for a user"""
        try:
            payments = Payment.query.filter_by(user_id=user_id).order_by(Payment.created_at.desc()).all()
            
            if not payments:
                return "No payment history found."
            
            response = "Recent payments:\n"
            for payment in payments:
                response += f"- {payment.payment_type}: ${payment.amount} ({payment.status})\n"
                response += f"  Date: {payment.created_at}\n"
                if payment.transaction_id:
                    response += f"  Transaction ID: {payment.transaction_id}\n"
            
            return response
            
        except Exception as e:
            current_app.logger.error(f"Error getting payment info: {str(e)}")
            return "I'm having trouble retrieving payment information. Please try again later."

    def get_hostel_info(self):
        """Get general hostel information"""
        try:
            hostels = Hostel.query.all()
            if not hostels:
                return "No hostel information available."
            
            response = "Hostel Information:\n"
            for hostel in hostels:
                response += f"\n{hostel.name}:\n"
                response += f"Address: {hostel.address}\n"
                if hostel.description:
                    response += f"Description: {hostel.description}\n"
                
                # Get room statistics
                rooms = Room.query.filter_by(hostel_id=hostel.id).all()
                total_rooms = len(rooms)
                available_rooms = len([r for r in rooms if r.is_available])
                
                response += f"Total Rooms: {total_rooms}\n"
                response += f"Available Rooms: {available_rooms}\n"
            
            return response
            
        except Exception as e:
            current_app.logger.error(f"Error getting hostel info: {str(e)}")
            return "I'm having trouble retrieving hostel information. Please try again later." 