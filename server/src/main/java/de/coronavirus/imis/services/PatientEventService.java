package de.coronavirus.imis.services;

import de.coronavirus.imis.domain.*;
import de.coronavirus.imis.repositories.DoctorRepository;
import de.coronavirus.imis.repositories.LaboratoryRepository;
import de.coronavirus.imis.repositories.PatientEventRepository;
import de.coronavirus.imis.repositories.PatientRepository;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

import javax.transaction.Transactional;
import java.sql.Timestamp;
import java.time.Instant;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Service
@AllArgsConstructor
@Deprecated
public class PatientEventService {

	private final PatientEventRepository patientEventRepository;
	private final LaboratoryRepository laboratoryRepository;
	private final DoctorRepository doctorRepository;
	private final PatientRepository patientRepository;

	public void createInitialPatientEvent(Patient patient,
										  Optional<Illness> illness,
										  EventType eventType,
										  LocalDate dateOfReporting) {
		var concreteIllness = illness.orElse(Illness.CORONA);
		patient.setPatientStatus(eventType);
		patientRepository.save(patient);
		final Timestamp eventTimestamp;

		if (dateOfReporting != null) {
			eventTimestamp = Timestamp.valueOf(dateOfReporting.atTime(12, 0));
		} else {
			eventTimestamp = Timestamp.from(Instant.now());
		}

		PatientEvent event = new PatientEvent()
				.setEventTimestamp(eventTimestamp)
				.setEventType(eventType)
				.setIllness(concreteIllness)
				.setPatient(patient);
		patientEventRepository.save(event);
	}

	public void createLabTestEvent(Patient patient, Optional<Illness> illness) {
		var concreteIllness = illness.orElse(Illness.CORONA);
		patient.setPatientStatus(EventType.TEST_SUBMITTED);
		patientRepository.save(patient);
		PatientEvent event = new PatientEvent()
				.setEventTimestamp(Timestamp.from(Instant.now()))
				.setEventType(EventType.TEST_SUBMITTED)
				.setIllness(concreteIllness)
				.setPatient(patient);
		patientEventRepository.saveAndFlush(event);
	}

	@Transactional
	public PatientEvent createScheduledEvent(Patient patient, String labId, String doctorId) {
		final Laboratory laboratory = laboratoryRepository.findById(labId).orElseGet(() -> {
			Laboratory lab = new Laboratory();
			lab.setId(labId);
			return laboratoryRepository.save(lab);
		});
		final Doctor doctor = doctorRepository.findById(doctorId).orElseGet(() ->
				{
					var newDoctor = new Doctor();
					newDoctor.setId(doctorId);
					return doctorRepository.save(newDoctor);
				}
		);
		patient.setPatientStatus(EventType.SCHEDULED_FOR_TESTING);
		patientRepository.save(patient);
		var event = new PatientEvent()
				.setEventTimestamp(Timestamp.from(Instant.now()))
				.setEventType(EventType.SCHEDULED_FOR_TESTING)
				.setIllness(Illness.CORONA)
				.setResponsibleDoctor(doctor)
				.setPatient(patient);
		return patientEventRepository.save(event);
	}

	public void createQuarantineEvent (Patient patient, String until, String comment) {

		var commentField = String.format("Bis: %s; %s", until, comment);

		var event = new PatientEvent()
				.setIllness(Illness.CORONA)
				.setEventType(EventType.QUARANTINE_MANDATED)
				.setEventTimestamp(Timestamp.valueOf(LocalDateTime.now()))
				.setPatient(patient)
				.setComment(commentField);

		patientEventRepository.saveAndFlush(event);
	}

	public PatientEvent createOrderTestEvent (Patient patient) {
		patient.setPatientStatus(EventType.ORDER_TEST);
		patientRepository.save(patient);
		var event = new PatientEvent()
				.setIllness(Illness.CORONA)
				.setEventType(EventType.ORDER_TEST)
				.setEventTimestamp(Timestamp.valueOf(LocalDateTime.now()))
				.setPatient(patient);
		patientEventRepository.saveAndFlush(event);
		return event;

	}

	public List<PatientEvent> getAllForPatient(Patient patient) {
		return patientEventRepository.findAllByPatient(patient);
	}


	public PatientEvent findFirstByPatientOrderByEventTimestampDesc(Patient patient) {
		return patientEventRepository.findFirstByPatientOrderByEventTimestampDesc(patient);
	}
}
