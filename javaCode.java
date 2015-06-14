

package org.openimaj.demos.sandbox;

import gnu.trove.map.hash.TIntObjectHashMap;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import cern.jet.random.Uniform;
import cern.jet.random.engine.MersenneTwister;
import cern.jet.random.engine.RandomEngine;

public class InfectionModel {
	RandomEngine random = new MersenneTwister();

	/**
	 * All the users
	 */
	List<User> users;

	/**
	 * Site probabilities
	 */
	SitesModel sites;

	/**
	 * Mapping of site addresses to hosts
	 */
	TIntObjectHashMap<Host> hostMap;

	/**
	 * Mapping of users to ISPs
	 */
	Map<User, ISP> ispMap;

	/**
	 * Mapping of site addresses to site objects
	 */
	TIntObjectHashMap<Site> dns;

	class ZipfGenerator {
		Uniform rnd = new Uniform(random);
		private int size;
		private double skew;
		private double bottom = 0;

		public ZipfGenerator(int size, double skew) {
			this.size = size;
			this.skew = skew;

			for (int i = 1; i < size; i++) {
				this.bottom += (1 / Math.pow(i, this.skew));
			}
		}

		// the next() method returns an random rank id.
		// The frequency of returned rank ids are follows Zipf distribution.
		public int next() {
			int rank;
			double frequency = 0;
			double dice;

			rank = rnd.nextIntFromTo(0, size);
			frequency = (1.0d / Math.pow(rank, this.skew)) / this.bottom;
			dice = rnd.nextDouble();

			while (!(dice < frequency)) {
				rank = rnd.nextIntFromTo(0, size);
				frequency = (1.0d / Math.pow(rank, this.skew)) / this.bottom;
				dice = rnd.nextDouble();
			}

			return rank - 1;
		}
	}

	/**
	 * Model of web sites with zipfian hit probabilities
	 */
	class SitesModel {
		int nSites;
		// private double exponent;
		ZipfGenerator zg;

		public SitesModel(int nSites, double exponent) {
			this.nSites = nSites;
			// this.exponent = exponent;
			zg = new ZipfGenerator(nSites, exponent);
		}

		int drawSite(int lastSite) {
			// return Distributions.nextZipfInt(exponent, random);
			return zg.next();
		}
	}

	enum SiteState {
		SAFE, VUNERABLE, INFECTED
	}

	class Site {
		/**
		 * Probability of getting fixed when infected
		 */
		double fixProbabilityInf;

		/**
		 * Probability of getting fixed when vunerable
		 */
		double fixProbabilityVun;

		/**
		 * Probability of becoming vunerable
		 */
		double vunerableProbability;

		/**
		 * Probability of becoming infected when vunerable
		 */
		double infectedProbability;

		SiteState state;

		public Site(double fixProbabilityInf, double fixProbabilityVun, double vunerableProbability,
				double infectedProbability, double initialInfectProbability, double initialVunerableProbability)
		{
			super();
			this.fixProbabilityInf = fixProbabilityInf;
			this.fixProbabilityVun = fixProbabilityVun;
			this.vunerableProbability = vunerableProbability;
			this.infectedProbability = infectedProbability;

			if (random.nextDouble() < initialInfectProbability)
				state = SiteState.INFECTED;
			else if (random.nextDouble() < initialVunerableProbability)
				state = SiteState.VUNERABLE;
			else
				state = SiteState.SAFE;
		}

		void iterate() {
			if (state == SiteState.SAFE) {
				// can become vunerable
				if (random.nextDouble() < vunerableProbability)
					state = SiteState.VUNERABLE;
			} else if (state == SiteState.VUNERABLE) {
				// can become fixed or infected
				if (random.nextDouble() < infectedProbability)
					state = SiteState.INFECTED;
				else if (random.nextDouble() < fixProbabilityVun)
					state = SiteState.SAFE;
			} else {
				// can become fixed
				if (random.nextDouble() < fixProbabilityInf)
					state = SiteState.SAFE;
			}
		}
	}

	class User {
		/**
		 * Probability a user will browse to a site at time t
		 */
		double browseProbability;

		/**
		 * Probability a user will disinfect themselves at time t
		 */
		double disinfectProbability;

		/**
		 * Probability a user will infect themselves from visiting an infected
		 * site
		 */
		double infectProbability;

		/**
		 * Id of the last site visited
		 */
		int lastSiteId = -1;

		/*
		 * Are we infected?
		 */
		boolean infected;

		public User(double browseProbability, double disinfectProbability, double infectProbability,
				double initialInfectProbability)
		{
			super();
			this.browseProbability = browseProbability;
			this.disinfectProbability = disinfectProbability;
			this.infectProbability = infectProbability;
			this.infected = random.nextDouble() < initialInfectProbability;
		}

		/**
		 * @return the next site to visit, or -1 if none
		 */
		int nextSite() {
			if (random.nextDouble() < browseProbability) {
				lastSiteId = sites.drawSite(lastSiteId);
				return lastSiteId;
			}

			return -1;
		}

		void disinfect() {
			if (infected && random.nextDouble() < disinfectProbability) {
				infected = false;
			}
		}

		void iterate() {
			disinfect();

			final int ns = nextSite();
			if (ns >= 0) {
				final Site site = ispMap.get(this).getSite(ns);

				if (site.state == SiteState.INFECTED && random.nextDouble() < infectProbability)
					this.infected = true;
			}
		}
	}

	class ISP {
		Site getSite(int site) {
			return hostMap.get(site).getSite(site);
		}
	}

	class Host {
		Site getSite(int site) {
			return dns.get(site);
		}
	}

	public InfectionModel() {
		final int nHosts = 10;
		final int nISPs = 10;

		// Site params (assumed fixed)
		final int nSites = 100;
		final double sitesExponent = 1;
		final double fixProbabilityInf = 0.1;
		final double fixProbabilityVun = 0.05;
		final double vunerableProbability = 0.05;
		final double infectedProbability = 0.001;
		final double initialInfectProbability = 0.00001;
		final double initialVunerableProbability = 0.0001;

		// User params
		final int nUsers = 100;
		final double browseProbability = 0.1;
		final double disinfectProbability = 0.0001;
		final double infectProbability = 0.5;
		final double userInitialInfectProbability = 0.001;

		// create hosts
		final Host[] hosts = new Host[nHosts];
		for (int i = 0; i < nHosts; i++)
			hosts[i] = new Host();

		// create sites and assign to hosts
		this.sites = new SitesModel(nSites, sitesExponent);
		this.dns = new TIntObjectHashMap<Site>();
		this.hostMap = new TIntObjectHashMap<Host>();
		for (int i = 0; i < nSites; i++) {
			final Site site = new Site(fixProbabilityInf, fixProbabilityVun, vunerableProbability,
					infectedProbability, initialInfectProbability, initialVunerableProbability);
			dns.put(i, site);

			// for now uniformly assign sites to hosts
			hostMap.put(i, hosts[i % nHosts]);
		}

		// create ISPs
		final ISP isps[] = new ISP[nISPs];
		for (int i = 0; i < nISPs; i++)
			isps[i] = new ISP();

		// Create users and assign to ISPs
		this.ispMap = new HashMap<User, ISP>();
		this.users = new ArrayList<User>();
		for (int i = 0; i < nUsers; i++) {
			final User u = new User(browseProbability, disinfectProbability, infectProbability,
					userInitialInfectProbability);
			this.users.add(u);

			// for now uniformly assign users to ISPs
			ispMap.put(u, isps[i % nISPs]);
		}
	}

	double performIteration() {
		for (final Site s : this.dns.valueCollection()) {
			s.iterate();
		}

		int count = 0;
		for (final User u : this.users) {
			u.iterate();
			count += u.infected ? 1 : 0;
		}

		return (double) count / (double) users.size();
	}

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		final InfectionModel model = new InfectionModel();

		for (int i = 0; i < 100000; i++) {
			System.out.println(i + " " + model.performIteration());
		}
	}
}

